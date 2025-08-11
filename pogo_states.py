# pogo_states.py
from enum import Enum, auto
import time

from io_fast import ShellSession, PngStream
from pogo_config import UiPack, PKG, ACTIVITY  # assuming you export PKG/ACTIVITY in your config
from pogo_ui import (
    tap_locator, exists, single_tap_center, swipe_by_name, end_of_list_after_swipe,
    playing_pogo
)

class Tag3StarState(Enum):
    OPEN_LIST = auto()
    OPEN_FIRST = auto()
    OPEN_MENU = auto()
    OPEN_APPRAISE = auto()
    TAP_TO_STATS = auto()
    EVAL_STARS = auto()
    TAG_OPEN_MENU = auto()
    TAG_OPEN_DIALOG = auto()
    TAG_APPLY = auto()
    TAG_CLOSE = auto()
    NEXT = auto()
    DONE = auto()

def open_pokemon_list(cfg: UiPack, sh: ShellSession, ps: PngStream) -> bool:
    # Top bar Poké Ball (Main Menu), then Main Menu → Pokémon
    if not tap_locator(cfg, cfg.top_bar.main_menu, sh, ps, cfg.waits.after_menu_open):
        return False
    if not tap_locator(cfg, cfg.main_menu.pokemon, sh, ps, cfg.waits.after_list_open):
        return False
    return True

def select_first_pokemon(cfg: UiPack, sh: ShellSession, ps: PngStream):
    # Anchor for first cell in list (image you capture)
    tap_locator(cfg, cfg.pokemon_list.first_pokemon_anchor, sh, ps, cfg.waits.after_open_detail)

def open_appraise_flow(cfg: UiPack, sh: ShellSession, ps: PngStream):
    tap_locator(cfg, cfg.appraise_menu.three_bars, sh, ps, cfg.waits.after_three_bars)
    tap_locator(cfg, cfg.appraise_menu.appraise_btn, sh, ps, cfg.waits.after_open_appraise)

def tag_three_star_once(cfg: UiPack, sh: ShellSession, ps: PngStream):
    # open hamburger -> tag -> choose Three Star -> close
    tap_locator(cfg, cfg.appraise_menu.three_bars, sh, ps, cfg.waits.after_three_bars)
    tap_locator(cfg, cfg.appraise_menu.tag_btn, sh, ps, cfg.waits.after_tag_open)
    tap_locator(cfg, cfg.appraise_menu.tag_three_star, sh, ps, cfg.waits.after_apply_tag)
    tap_locator(cfg, cfg.appraise_menu.tag_close, sh, ps, cfg.waits.after_close_tag)

def tag_three_star_pass(cfg: UiPack, sh: ShellSession, ps: PngStream, *, adb: str = "adb", serial: str | None = None):
    if not playing_pogo(PKG, ACTIVITY, cfg, adb=adb, serial=serial):
        return

    # Navigate to Pokémon list
    assert open_pokemon_list(cfg, sh, ps)

    state = Tag3StarState.OPEN_FIRST
    running = True

    while running:
        if state == Tag3StarState.OPEN_FIRST:
            select_first_pokemon(cfg, sh, ps)
            state = Tag3StarState.OPEN_MENU

        elif state == Tag3StarState.OPEN_MENU:
            open_appraise_flow(cfg, sh, ps)
            state = Tag3StarState.TAP_TO_STATS

        elif state == Tag3StarState.TAP_TO_STATS:
            single_tap_center(sh, ps, cfg.waits.after_tap_advance)  # enter stats in appraise
            state = Tag3StarState.EVAL_STARS

        elif state == Tag3StarState.EVAL_STARS:
            if exists(cfg, cfg.appraise_menu.three_stars_badge, ps, timeout=1.0):
                # exit appraise (one tap) then tag
                single_tap_center(sh, ps, cfg.waits.after_tap_advance)
                tag_three_star_once(cfg, sh, ps)
                state = Tag3StarState.NEXT
            else:
                state = Tag3StarState.NEXT  # keep appraise open for next mon

        elif state == Tag3StarState.NEXT:
            if end_of_list_after_swipe(cfg, "next_pokemon", sh, ps):
                state = Tag3StarState.DONE
            else:
                # If we tagged, we’re back on detail view; need to reopen appraise.
                # Heuristic: try hamburger; if not found quickly, we’re still in appraise and can jump to TAP_TO_STATS.
                if tap_locator(cfg, cfg.appraise_menu.three_bars, sh, ps, cfg.waits.after_three_bars):
                    tap_locator(cfg, cfg.appraise_menu.appraise_btn, sh, ps, cfg.waits.after_open_appraise)
                    state = Tag3StarState.TAP_TO_STATS
                else:
                    state = Tag3StarState.TAP_TO_STATS

        elif state == Tag3StarState.DONE:
            running = False
