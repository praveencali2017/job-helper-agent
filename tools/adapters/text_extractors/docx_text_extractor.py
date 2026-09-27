from tools.ports import DocxTextExtractor
from docx import Document

class DocxTextExtractor(DocxTextExtractor):
    """
    Extracts text from DOCX files.
    """
    
    def extract_text_from_docx(self, filepath: str) -> str:
        """
        Extract text from a DOCX file.

        Args:
            filepath: Path to the DOCX file.

        Returns:
            The extracted text content of the DOCX file.
        """
        try:
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from DOCX file '{filepath}': {e}")