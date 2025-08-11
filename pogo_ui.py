# pogo_ui.py
import time
from typing import Optional

import numpy as np

from io_fast import ShellSession, PngStream, decode_png
from pogo_adb import start_app, is_foreground
from pogo_config import UiPack, Swipe
from pogo_cv import find_locator, center_of, signatures_from_frame

def _next_frame(ps: PngStream) -> np.ndarray:
    while True:
        png = ps.next_png()
        if png is None:
            continue
        img = decode_png(png)
        if img is not None:
            return img

def wait_and_find(cfg: UiPack, locator, ps: PngStream, timeout: float = 3.0, poll: float = 0.12):
    t0 = time.time()
    hit = None
    while time.time() - t0 < timeout:
        frame = _next_frame(ps)
        hit = find_locator(cfg, locator, frame)
        if hit:
            return hit, frame
        time.sleep(poll)
    return None, None

def tap_locator(cfg: UiPack, locator, sh: ShellSession, ps: PngStream, wait_after: float = 0.0) -> bool:
    hit, frame = wait_and_find(cfg, locator, ps, timeout=3.0)
    if not hit:
        return False
    x, y = center_of(hit)
    sh.tap(x, y)
    if wait_after:
        time.sleep(wait_after)
    return True

def exists(cfg: UiPack, locator, ps: PngStream, timeout: float = 1.2) -> bool:
    hit, _ = wait_and_find(cfg, locator, ps, timeout=timeout, poll=0.12)
    return hit is not None

def single_tap_center(sh: ShellSession, ps: PngStream, wait_after: float = 0.0):
    frame = _next_frame(ps)
    H, W = frame.shape[:2]
    sh.tap(W // 2, int(H * 0.65))
    if wait_after:
        time.sleep(wait_after)

def _abs_points_from_swipe(frame: np.ndarray, swipe: Swipe):
    H, W = frame.shape[:2]
    sx = int(W * swipe.start[0]); sy = int(H * swipe.start[1])
    ex = int(W * swipe.end[0]);   ey = int(H * swipe.end[1])
    return sx, sy, ex, ey

def swipe_by_name(cfg: UiPack, key: str, sh: ShellSession, ps: PngStream, wait_after: float = 0.0):
    frame = _next_frame(ps)
    if key not in cfg.swipes:
        raise KeyError(f"Unknown swipe '{key}'")
    sx, sy, ex, ey = _abs_points_from_swipe(frame, cfg.swipes[key])
    sh.swipe(sx, sy, ex, ey, cfg.swipes[key].duration_ms)
    if wait_after:
        time.sleep(wait_after)

def end_of_list_after_swipe(cfg: UiPack, key: str, sh: ShellSession, ps: PngStream) -> bool:
    before = signatures_from_frame(cfg, _next_frame(ps))
    swipe_by_name(cfg, key, sh, ps, wait_after=cfg.waits.after_swipe)
    after = signatures_from_frame(cfg, _next_frame(ps))
    return before == after

def playing_pogo(pkg: str, activity: str, cfg: UiPack, *, adb: str = "adb", serial: str | None = None) -> bool:
    if is_foreground(pkg, adb=adb, serial=serial):
        return True
    start_app(pkg, activity, adb=adb, serial=serial)
    time.sleep(cfg.waits.after_launch)
    return is_foreground(pkg, adb=adb, serial=serial)
