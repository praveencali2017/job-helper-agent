from functools import wraps
import os
from tools.ports import DocxTextExtractor, PdfTextExtractor
from langchain_core.tools import StructuredTool

def require_extension(*allowed):
    """Decorator that restricts a method to files with specific extensions.

    Args:
        *allowed: One or more file extensions (e.g. ".txt", ".md").
            Leading dots are optional and matching is case-insensitive.

    Returns:
        A decorator that wraps a method, raising ValueError if the
        provided filepath's extension is not in the allowed set.
    """
    allowed = {e.lower() for e in allowed}

    def decorator(func):
        @wraps(func)
        def wrapper(self, filepath: str, *args, **kwargs):
            ext = os.path.splitext(filepath)[-1].lower()
            if ext not in allowed:
                raise ValueError(
                    f"Unsupported file type '{ext}'. Allowed: {', '.join(sorted(allowed))}"
                )
            return func(self, filepath, *args, **kwargs)
        return wrapper
    return decorator


   

class TextExtractorService:
    """
    Service that uses provided text extractors to extract text from DOCX and PDF files.
    """
    
    def __init__(self, docx_text_extractor: DocxTextExtractor, 
                 pdf_text_extractor: PdfTextExtractor):
        self.docx_text_extractor = docx_text_extractor
        self.pdf_text_extractor = pdf_text_extractor


    @require_extension(".pdf") 
    def extract_text_from_pdf(self, filepath: str):
        """Extract text from a PDF file.

        Args:
            filepath: Path to a PDF file.

        Returns:
            The extracted text content of the PDF.

        Raises:
            ValueError: If the file does not have a ".pdf" extension.
        """
        return self.pdf_text_extractor.extract_text_from_pdf(filepath)


    @require_extension(".docx")
    def extract_text_from_docx(self, filepath: str):
        """Extract text from a DOCX file.

        Args:
            filepath: Path to a DOCX file.

        Returns:
            The extracted text content of the DOCX.

        Raises:
            ValueError: If the file does not have a ".docx" extension.
        """
        return self.docx_text_extractor.extract_text_from_docx(filepath)


    @require_extension(".docx", ".pdf")
    def extract_text(self, filepath: str):
        """
        Extract text from a file, delegating to the appropriate extractor based on file extension.

        Args:
            filepath (str): Path to the file (DOCX or PDF).
        """
        ext = os.path.splitext(filepath)[-1].lower()
        if ext == ".docx":
            return self.extract_text_from_docx(filepath)
        elif ext == ".pdf":
            return self.extract_text_from_pdf(filepath)
        else:
            raise ValueError(f"Unsupported file type '{ext}'. Allowed: .docx, .pdf")


    def as_tools(self) -> list[StructuredTool]:
        """
        Return the TextExtractorService as a list of StructuredTool instances.

        Returns:
            A list containing StructuredTool instances for DOCX and PDF text extraction.
        """
        return [
            StructuredTool.from_function(
                name="extract_text_from_docx",
                description="Extract text from a DOCX file.",
                func=self.extract_text_from_docx
            ),
            StructuredTool.from_function(
                name="extract_text_from_pdf",
                description="Extract text from a PDF file.",
                func=self.extract_text_from_pdf
            ),
            StructuredTool.from_function(
                name="extract_text",
                description="Extract text from a DOCX or PDF file.",
                func=self.extract_text
            ),
        ]

