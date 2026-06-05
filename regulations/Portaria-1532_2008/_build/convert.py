"""Convert Portaria-1532_2008_original.pdf to one markdown file using docling (no OCR).

Source rationale: the DRE "consolidated" PDF (Portaria-1532_2008.pdf) renders every
table/figure as the placeholder "(ver documento original)" — 54 of them, including all
51 Quadros. The original Diario da Republica PDF (Portaria-1532_2008_original.pdf)
contains the real tables, which docling extracts well as markdown tables. So the
original is the single source of truth.

The original is born-digital (full text layer, 78 pages, 2-column DR layout) so OCR is
off. Table structure parsing is on. Page/picture image rendering is off (no content
figures exist; the regulation has tables only) which also avoids the std::bad_alloc
seen when rendering many pages to bitmap.

Conversion is done in page-range chunks, each in a fresh subprocess (worker.py) to
keep memory bounded; per-chunk markdown is concatenated into full_document.md.

Run with the Python that has docling installed (Python314):
    python docs/regulations/Portaria-1532_2008/_build/convert.py
"""

import subprocess
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent          # .../Portaria-1532_2008
BUILD = OUT / "_build"
WORKER = BUILD / "worker.py"
FULL_MD = OUT / "full_document.md"
CHUNKS_DIR = BUILD / "chunks"

TOTAL_PAGES = 78
CHUNK_SIZE = 12


def main() -> None:
    CHUNKS_DIR.mkdir(parents=True, exist_ok=True)
    # clear stale chunks from previous (DRE) run
    for f in CHUNKS_DIR.glob("chunk_*.md"):
        f.unlink()

    chunk_files = []
    for start in range(1, TOTAL_PAGES + 1, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE - 1, TOTAL_PAGES)
        out_md = CHUNKS_DIR / f"chunk_{start:03d}_{end:03d}.md"
        print(f"Converting pages {start}-{end} ...", flush=True)
        subprocess.run(
            [sys.executable, str(WORKER), str(start), str(end), str(out_md)],
            check=True,
        )
        chunk_files.append(out_md)

    parts = [f.read_text(encoding="utf-8").strip() for f in chunk_files]
    FULL_MD.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
    print(f"\nWrote {FULL_MD} ({FULL_MD.stat().st_size:,} bytes) from {len(parts)} chunks")


if __name__ == "__main__":
    main()
