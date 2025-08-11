# pogo_cv.py
import hashlib
import os
from typing import Optional, Tuple, Iterable

import cv2
import numpy as np
from pogo_config import UiPack, Locator

def _tpl_path(cfg: UiPack, loc: Locator) -> str:
    return os.path.join(cfg.asset_dir, loc.file)

def load_template(cfg: UiPack, loc: Locator) -> np.ndarray:
    path = _tpl_path(cfg, loc)
    img = cv2.imread(path, cv2.IMREAD_COLOR)
    if img is None:
        raise FileNotFoundError(f"Missing template: {path}")
    return img

def match_template(scr: np.ndarray, tpl: np.ndarray, thresh: float,
                   scales: Iterable[float] = (1.0, 0.9, 1.1, 0.8, 1.2)) \
                   -> Optional[Tuple[int,int,int,int,float]]:
    h, w = scr.shape[:2]
    best = None
    for s in scales:
        rs = cv2.resize(scr, (max(1,int(w*s)), max(1,int(h*s))), interpolation=cv2.INTER_AREA if s<1 else cv2.INTER_LINEAR)
        res = cv2.matchTemplate(rs, tpl, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        if best is None or max_val > best[-1]:
            x, y = max_loc
            th, tw = tpl.shape[:2]
            bx0 = int(x / s); by0 = int(y / s)
            bw = int(tw / s);  bh = int(th / s)
            best = (bx0, by0, bw, bh, max_val)
    if best and best[-1] >= thresh:
        return best
    return None

def find_locator(cfg: UiPack, loc: Locator, screen: np.ndarray) -> Optional[Tuple[int,int,int,int,float]]:
    tpl = load_template(cfg, loc)
    return match_template(screen, tpl, loc.thresh)

def center_of(bbox: Tuple[int,int,int,int,float]) -> Tuple[int,int]:
    x, y, w, h, _ = bbox
    return x + w//2, y + h//2

def crop_percent(screen: np.ndarray, rect: Tuple[float,float,float,float]) -> np.ndarray:
    H, W = screen.shape[:2]
    x, y, w, h = rect
    x0 = int(W * x); y0 = int(H * y); x1 = int(W * (x + w)); y1 = int(H * (y + h))
    return screen[y0:y1, x0:x1]

def signature_bytes(img: np.ndarray) -> bytes:
    small = cv2.resize(img, (160, 90), interpolation=cv2.INTER_AREA)
    return hashlib.blake2b(small.tobytes(), digest_size=16).digest()

def signatures_from_frame(cfg: UiPack, screen: np.ndarray) -> Tuple[bytes, bytes]:
    cp = crop_percent(screen, cfg.sig_rects.cp)
    wt = crop_percent(screen, cfg.sig_rects.weight)
    return signature_bytes(cp), signature_bytes(wt)
