from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter

class DocumentProcessor:
    def __init__(self, pdf_docs):
        self.pdf_docs = pdf_docs  # List of PDF file paths or file-like objects
        self.text = ""
        self.text_chunks = []

    def extract_text(self):
        """Extracts text from multiple PDF documents."""
        all_text = []
        for pdf in self.pdf_docs:
            reader = PdfReader(pdf)
            for page in reader.pages:
                page_text = page.extract_text() or ""
                all_text.append(page_text)
        self.text = "\n".join(all_text)
        return self.text

    def split_text(self):
        """Splits extracted text into manageable chunks."""
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=3000)
        self.text_chunks = text_splitter.split_text(self.text)
        return self.text_chunks

    def run(self):
        self.extract_text()
        self.split_text()
        return self.text_chunks
