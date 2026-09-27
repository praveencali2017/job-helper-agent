from abc import ABC, abstractmethod

class DocxTextExtractor(ABC):
    """Port for extracting text from Microsoft Word (.docx) documents.

    Implementations adapt a concrete .docx text-extraction library behind a
    single method.
    """

    @abstractmethod
    def extract_text_from_docx(self, filepath: str) -> str:
        """Extract the text content from a .docx file.

        Args:
            filepath: Path to the .docx document.

        Returns:
            The extracted text.
        """
        pass


class PdfTextExtractor(ABC):
    """Port for extracting text from PDF documents.

    Implementations adapt a concrete PDF text-extraction library behind a
    single method.
    """

    @abstractmethod
    def extract_text_from_pdf(self, filepath: str) -> str:
        """Extract the text content from a PDF file.

        Args:
            filepath: Path to the PDF document.

        Returns:
            The extracted text.
        """
        pass
