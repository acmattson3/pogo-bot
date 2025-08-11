# io_fast.py
import io
import subprocess
from typing import Optional

import numpy as np
import cv2


class ShellSession:
    """
    One persistent 'adb shell' you can feed multiple commands to.
    Use .tap/.swipe/.key/.sleep helpers to avoid string building at call sites.
    """
    def __init__(self, adb: str = "adb", serial: Optional[str] = None):
        self.args = [adb] + (["-s", serial] if serial else []) + ["shell"]
        # text=True so we can .write(str); we never read stdout to avoid blocking
        self.p = subprocess.Popen(self.args,
                                  stdin=subprocess.PIPE,
                                  stdout=subprocess.DEVNULL,
                                  stderr=subprocess.DEVNULL,
                                  text=True,
                                  bufsize=1)

    def send(self, cmd: str) -> None:
        self.p.stdin.write(cmd + "\n")
        self.p.stdin.flush()

    # Convenience
    def tap(self, x: int, y: int): self.send(f"input tap {x} {y}")
    def swipe(self, x1: int, y1: int, x2: int, y2: int, dur_ms: int = 250):
        self.send(f"input swipe {x1} {y1} {x2} {y2} {dur_ms}")
    def key(self, keycode: str): self.send(f"input keyevent {keycode}")  # e.g. KEYCODE_BACK
    def sleep(self, seconds: float): self.send(f"sleep {seconds}")

    def close(self):
        try:
            self.p.stdin.write("exit\n"); self.p.stdin.flush()
        except Exception:
            pass
        self.p.terminate()

    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): self.close()


class PngStream:
    """
    Continuous screencap reader:
    adb exec-out sh -c 'while :; do screencap -p; done'
    Call next_png() to get one PNG frame (bytes). Use decode_png() to get a cv2 mat.
    """
    def __init__(self, adb: str = "adb", serial: Optional[str] = None):
        args = [adb] + (["-s", serial] if serial else []) + \
               ["exec-out", "sh", "-c", "while :; do screencap -p; done"]
        self.p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)

    def next_png(self) -> Optional[bytes]:
        out = self.p.stdout
        if out is None:
            return None
        read = out.read

        sig = read(8)
        if not sig:
            return None
        if sig != b"\x89PNG\r\n\x1a\n":
            # rare desync; drop until next loop frame
            return None

        buf = io.BytesIO()
        buf.write(sig)
        while True:
            raw_len = read(4)
            if not raw_len:
                return None
            length = int.from_bytes(raw_len, "big")
            ctype = read(4)
            data = read(length)
            crc = read(4)
            if not ctype or not data or not crc:
                return None
            buf.write(raw_len); buf.write(ctype); buf.write(data); buf.write(crc)
            if ctype == b"IEND":
                return buf.getvalue()

    def close(self): self.p.terminate()
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): self.close()


def decode_png(png_bytes: bytes):
    """PNG bytes -> cv2 BGR image"""
    arr = np.frombuffer(png_bytes, dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if img is None:
        raise RuntimeError("Failed to decode PNG frame")
    return img
