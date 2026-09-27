from tools.ports import PdfTextExtractor
import pdfplumber

class PdfPlumberTextExtractor(PdfTextExtractor):
    """
    Extracts text from PDF files using the pdfplumber library.
    """
    
    def extract_text_from_pdf(self, filepath: str) -> str:
        """
        Extract text from a PDF file.

        Args:
            filepath: Path to the PDF file.

        Returns:
            The extracted text content of the PDF file.
        """
        try:
            with pdfplumber.open(filepath) as pdf:
                return "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF file '{filepath}': {e}")