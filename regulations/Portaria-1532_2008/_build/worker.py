"""Convert a single page range of the original PDF to markdown (fresh process per chunk).

Running each chunk in its own process resets memory between chunks, avoiding the
std::bad_alloc that can occur when converting many pages in one process.

Usage:
    python worker.py <start_page> <end_page> <out_md>
"""

import sys
from pathlib import Path

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import ImageRefMode

OUT = Path(__file__).resolve().parent.parent
SRC = OUT.parent / "Portaria-1532_2008_original.pdf"


def main() -> None:
    start, end, out_md = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = False
    pipeline_options.do_table_structure = True
    pipeline_options.generate_page_images = False
    pipeline_options.generate_picture_images = False

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }
    )

    result = converter.convert(str(SRC), page_range=(start, end))
    result.document.save_as_markdown(out_md, image_mode=ImageRefMode.PLACEHOLDER)
    print(f"  chunk {start}-{end} -> {out_md.name} ({out_md.stat().st_size:,} bytes)", flush=True)


if __name__ == "__main__":
    main()
