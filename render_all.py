#!/usr/bin/env python3
"""
Render every Slide* scene in my_slides/ in one shot.

Usage:
    uv run python render_all.py            # low quality (default)
    uv run python render_all.py -qm        # medium
    uv run python render_all.py -qh        # high
    uv run python render_all.py -qk        # 4k
    uv run python render_all.py Slide13RandomFunction Slide12...
        # render only the named scenes (still in order if multiple given)

NOTE on quality flags: `manim-slides render` greedily eats `-h` as its own
help flag, so passing `-qh` directly to it shows the usage screen instead
of rendering at high quality. This script translates `-qX` into the safe
long form `--quality X` before invoking manim-slides.

Runs `manim-slides render` once per scene so each slide's .json and
slides/files/<name>/ directory is produced. Aborts on the first failure.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SLIDES_DIR = ROOT / "my_slides"
CLASS_RE = re.compile(r"^class\s+(Slide\d+\w*)\s*\(\s*Slide\s*\)\s*:", re.MULTILINE)


def discover_scenes() -> list[tuple[Path, str]]:
    """Return [(path, class_name), ...] sorted by scene number."""
    found: list[tuple[int, Path, str]] = []
    for path in SLIDES_DIR.glob("scene*.py"):
        text = path.read_text()
        for match in CLASS_RE.finditer(text):
            cls = match.group(1)
            num_match = re.match(r"Slide(\d+)", cls)
            num = int(num_match.group(1)) if num_match else 9999
            found.append((num, path, cls))
    found.sort(key=lambda t: (t[0], t[2]))
    return [(p, c) for _, p, c in found]


def parse_args(argv: list[str]) -> tuple[list[str], list[str]]:
    """Returns (quality_flag_as_long_form, selected_scene_names)."""
    # Default low quality. Map -qX → ["--quality", "X"] so manim-slides
    # doesn't interpret the bare -h inside "-qh" as its own help flag.
    quality_map = {
        "-ql": "l", "-qm": "m", "-qh": "h", "-qp": "p", "-qk": "k",
    }
    quality_letter = "l"
    selected: list[str] = []
    for arg in argv:
        if arg in quality_map:
            quality_letter = quality_map[arg]
        elif arg.startswith("--quality="):
            quality_letter = arg.split("=", 1)[1]
        else:
            selected.append(arg)
    return ["--quality", quality_letter], selected


def main() -> int:
    quality, selected = parse_args(sys.argv[1:])
    scenes = discover_scenes()

    if selected:
        wanted = set(selected)
        scenes = [(p, c) for (p, c) in scenes if c in wanted]
        missing = wanted - {c for (_, c) in scenes}
        if missing:
            print(f"unknown scene(s): {', '.join(sorted(missing))}", file=sys.stderr)
            return 2

    if not scenes:
        print("no scenes found", file=sys.stderr)
        return 1

    env = os.environ.copy()
    # Ensure `from my_slides...` imports resolve when running from anywhere.
    env["PYTHONPATH"] = f"{ROOT}{os.pathsep}{env.get('PYTHONPATH', '')}"

    total = len(scenes)
    print(f"Rendering {total} scene(s) at {' '.join(quality)} from {SLIDES_DIR}\n")

    for i, (path, cls) in enumerate(scenes, 1):
        rel = path.relative_to(ROOT)
        print(f"[{i}/{total}] {cls}  ({rel})")
        cmd = ["uv", "run", "manim-slides", "render", *quality, str(rel), cls]
        result = subprocess.run(cmd, cwd=ROOT, env=env)
        if result.returncode != 0:
            print(f"\n✗ {cls} failed (exit {result.returncode})", file=sys.stderr)
            return result.returncode
        print()

    print(f"✓ rendered {total} scene(s) successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())
