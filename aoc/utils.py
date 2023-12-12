#!/usr/bin/env python
import subprocess
from pathlib import Path

TOP_DIR = Path(__file__).parent.parent


def shell(cmd: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(cmd, shell=True)


def get_cookie_headers() -> dict[str, str]:
    with TOP_DIR.joinpath(".cookie").open() as in_file:
        contents = in_file.read().strip()
    return {"Cookie": contents, "User-Agent": "kaitj"}
