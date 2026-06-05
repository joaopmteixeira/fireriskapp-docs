"""Generic regulation PDF converter — reads config.json, spawns worker.py per chunk.

Usage:
    python docs/regulations/_pipeline/convert.py docs/regulations/<regulation-dir>/

The regulation directory must contain a config.json with at least:
    pdf_original  — path to the source PDF, relative to the regulation dir
    total_pages   — total page count
    chunk_size    — (optional, default 12) pages per subprocess
"""

import json
import subprocess
import sys
from pathlib import Path

WORKER = Path(__file__).resolve().parent / "worker.py"


def main() -> None:
    reg_dir = Path(sys.argv[1]).resolve()
    config = json.loads((reg_dir / "config.json").read_text(encoding="utf-8"))

    pdf_path = (reg_dir / config["pdf_original"]).resolve()
    total_pages = config["total_pages"]
    chunk_size = config.get("chunk_size", 12)
    chunks_dir = reg_dir / "_build" / "chunks"
    full_md = reg_dir / "full_document.md"

    chunks_dir.mkdir(parents=True, exist_ok=True)
    for f in chunks_dir.glob("chunk_*.md"):
        f.unlink()

    chunk_files = []
    for start in range(1, total_pages + 1, chunk_size):
        end = min(start + chunk_size - 1, total_pages)
        out_md = chunks_dir / f"chunk_{start:03d}_{end:03d}.md"
        print(f"Converting pages {start}-{end} ...", flush=True)
        subprocess.run(
            [sys.executable, str(WORKER), str(start), str(end), str(out_md), str(pdf_path)],
            check=True,
        )
        chunk_files.append(out_md)

    parts = [f.read_text(encoding="utf-8").strip() for f in chunk_files]
    full_md.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"\nWrote {full_md} ({full_md.stat().st_size:,} bytes) from {len(parts)} chunks")


if __name__ == "__main__":
    main()
