from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.chunking import HybridChunker


# ------------------------------------------------------------
# PDF pipeline configuration
# ------------------------------------------------------------

pipeline_options = PdfPipelineOptions()

# Disable OCR for text-based PDFs
pipeline_options.do_ocr = False


# ------------------------------------------------------------
# Document converter
# ------------------------------------------------------------

converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(
            pipeline_options=pipeline_options
        )
    }
)


# ------------------------------------------------------------
# Structure-aware chunker
# ------------------------------------------------------------

chunker = HybridChunker()


def chunk_pdf(pdf_path: str):

    result = converter.convert(pdf_path)

    chunks = []

    for chunk in chunker.chunk(result.document):

        text = chunk.text.strip()

        if text:
            chunks.append(text)

    return chunks