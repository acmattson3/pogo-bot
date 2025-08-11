# pogo_adb.py
import re
import subprocess
from typing import Optional, Tuple

def _adb(args, adb: str = "adb", serial: Optional[str] = None, text: bool = True):
    base = [adb] + (["-s", serial] if serial else [])
    return subprocess.run(base + args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=text)

def start_app(pkg: str, activity: str, *, adb: str = "adb", serial: Optional[str] = None):
    _adb(["shell", "am", "start", "-n", f"{pkg}/{activity}"], adb, serial)

def is_foreground(pkg: str, *, adb: str = "adb", serial: Optional[str] = None) -> bool:
    out = _adb(["shell", "dumpsys", "window", "windows"], adb, serial).stdout or ""
    return pkg in out

def am_force_stop(pkg: str, *, adb: str = "adb", serial: Optional[str] = None):
    _adb(["shell", "am", "force-stop", pkg], adb, serial)

def monkey_launch(pkg: str, *, adb: str = "adb", serial: Optional[str] = None):
    _adb(["shell", "monkey", "-p", pkg, "-c", "android.intent.category.LAUNCHER", "1"], adb, serial)

def close_system_dialogs(*, adb: str = "adb", serial: Optional[str] = None):
    _adb(["shell", "am", "broadcast", "-a", "android.intent.action.CLOSE_SYSTEM_DIALOGS"], adb, serial)

def wm_size(*, adb: str = "adb", serial: Optional[str] = None) -> Tuple[int, int]:
    out = _adb(["shell", "wm", "size"], adb, serial).stdout or ""
    m = re.search(r"Physical size:\s*(\d+)x(\d+)", out)
    if not m:
        raise RuntimeError("Failed to get wm size")
    return int(m.group(1)), int(m.group(2))

def stay_awake_usb(enable: bool, *, adb: str = "adb", serial: Optional[str] = None):
    _adb(["shell", "svc", "power", "stayon", "usb" if enable else "false"], adb, serial)

def lock_orientation_portrait(*, adb: str = "adb", serial: Optional[str] = None):
    _adb(["shell", "settings", "put", "system", "accelerometer_rotation", "0"], adb, serial)
    _adb(["shell", "settings", "put", "system", "user_rotation", "0"], adb, serial)
