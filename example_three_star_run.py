# example_three_star_run.py
from io_fast import ShellSession, PngStream
from pogo_config import default_pack
from pogo_states import tag_three_star_pass

if __name__ == "__main__":
    cfg = default_pack("./assets")  # replace with your assets folder
    with ShellSession() as sh, PngStream() as ps:
        tag_three_star_pass(cfg, sh, ps)
