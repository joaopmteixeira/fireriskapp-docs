"""Convert a page range of the ORIGINAL DR PDF to markdown (for table quality test)."""

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
    po = PdfPipelineOptions()
    po.do_ocr = False
    po.do_table_structure = True
    po.generate_page_images = False
    po.generate_picture_images = False
    converter = DocumentConverter(
        format_options={InputFormat.PDF: PdfFormatOption(pipeline_options=po)}
    )
    result = converter.convert(str(SRC), page_range=(start, end))
    result.document.save_as_markdown(out_md, image_mode=ImageRefMode.PLACEHOLDER)
    print(f"  orig {start}-{end} -> {out_md.name} ({out_md.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
