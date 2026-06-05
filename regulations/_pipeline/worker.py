"""Docling subprocess worker for regulation PDF conversion (generic, parameterised).

Identical to Portaria-1532_2008/_build/worker.py but accepts pdf_path as argv[4]
instead of having it hardcoded, making it reusable across regulations.

Running each chunk in its own process resets memory between chunks, avoiding
std::bad_alloc when converting many pages in one process.

Usage:
    python worker.py <start_page> <end_page> <out_md> <pdf_path>
"""

import sys
from pathlib import Path

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling_core.types.doc import ImageRefMode


def main() -> None:
    start = int(sys.argv[1])
    end = int(sys.argv[2])
    out_md = Path(sys.argv[3])
    pdf_path = Path(sys.argv[4])

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

    result = converter.convert(str(pdf_path), page_range=(start, end))
    result.document.save_as_markdown(out_md, image_mode=ImageRefMode.PLACEHOLDER)
    print(f"  chunk {start}-{end} -> {out_md.name} ({out_md.stat().st_size:,} bytes)", flush=True)


if __name__ == "__main__":
    main()
