import PyPDF2
import pdfplumber
import streamlit as st
from typing import Union
import io

class PDFProcessor:
    def __init__(self):
        pass
    
    def extract_text(self, pdf_file) -> str:
        """Extract text from PDF file using multiple methods for better accuracy"""
        try:
            # Method 1: Using pdfplumber (better for complex layouts)
            text = self._extract_with_pdfplumber(pdf_file)
            if text.strip():
                return text
            
            # Method 2: Fallback to PyPDF2
            pdf_file.seek(0)  # Reset file pointer
            text = self._extract_with_pypdf2(pdf_file)
            return text
            
        except Exception as e:
            raise Exception(f"Failed to extract text from PDF: {str(e)}")
    
    def _extract_with_pdfplumber(self, pdf_file) -> str:
        """Extract text using pdfplumber"""
        text = ""
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _extract_with_pypdf2(self, pdf_file) -> str:
        """Extract text using PyPDF2"""
        text = ""
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
