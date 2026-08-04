"""Run the reference pipeline on Windows without the cp1252 crash.

`scripts/run_all.py` prints a Unicode step marker that Windows' default cp1252
console encoding cannot encode, so a bare `python scripts/run_all.py` dies with
UnicodeEncodeError before step 1. CI runs Ubuntu/UTF-8 and never sees it.

`work/README.md` requires the reference pipeline in `scripts/` to stay pristine,
so this fixes the environment instead of the script: it forces UTF-8 on this
process's streams and exports the UTF-8 env vars, which the pipeline's
`subprocess.run` children inherit.

    python work/scripts/run_all_utf8.py

Behaviour is otherwise identical to running `scripts/run_all.py` directly.
"""
from __future__ import annotations

import os
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / "scripts" / "run_all.py"


def main() -> int:
    if not PIPELINE.exists():
        print(f"Reference pipeline not found: {PIPELINE}", file=sys.stderr)
        return 1

    # This process: make the step markers printable.
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")

    # Child steps: run_all.py shells out with subprocess.run, which inherits these.
    os.environ["PYTHONUTF8"] = "1"
    os.environ["PYTHONIOENCODING"] = "utf-8"

    # run_all.py does `from ml_utils import ...`, so scripts/ must be importable.
    sys.path.insert(0, str(ROOT / "scripts"))

    runpy.run_path(str(PIPELINE), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
