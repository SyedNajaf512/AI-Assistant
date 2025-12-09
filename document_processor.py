"""
Anna AI Assistant - Document Processor
Handles PDF and text file reading, extraction, and storage
"""

import os
import hashlib
from pathlib import Path
from PyPDF2 import PdfReader
from logger import logger
from config import config
import google.generativeai as genai


class DocumentProcessor:
    """Process and extract content from documents"""
    
    def __init__(self):
        # Configure Gemini for summarization
        if config.gemini_api_key:
            genai.configure(api_key=config.gemini_api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        else:
            self.model = None
        
        # Max text length before summarization (chars)
        self.max_full_text_length = 50000  # ~50 pages
    
    def process_file(self, file_path):
        """Process a file and extract its content"""
        try:
            if not os.path.exists(file_path):
                return {"success": False, "message": f"File not found: {file_path}"}
            
            file_path = Path(file_path)
            file_ext = file_path.suffix.lower()
            
            # Extract text based on file type
            if file_ext == '.pdf':
                text = self.extract_from_pdf(str(file_path))
            elif file_ext in ['.txt', '.md', '.log']:
                text = self.extract_from_text(str(file_path))
            else:
                return {"success": False, "message": f"Unsupported file type: {file_ext}"}
            
            if not text:
                return {"success": False, "message": "Could not extract text from file"}
            
            # Generate metadata
            filename = file_path.name
            file_hash = self._hash_file(str(file_path))
            
            # Decide if we need to summarize
            if len(text) > self.max_full_text_length:
                # Large file - create summary
                summary = self._summarize_text(text[:self.max_full_text_length * 2])  # Use more text for summary
                stored_content = summary
                is_summarized = True
            else:
                # Small file - store full content
                stored_content = text
                summary = self._create_brief_summary(text)
                is_summarized = False
            
            # Create document data
            document_data = {
                "filename": filename,
                "file_path": str(file_path),
                "file_hash": file_hash,
                "content": stored_content,
                "summary": summary,
                "is_summarized": is_summarized,
                "file_type": file_ext,
                "size_chars": len(text)
            }
            
            return {
                "success": True,
                "message": f"Processed {filename}",
                "data": document_data
            }
            
        except Exception as e:
            logger.log_error("DOCUMENT_PROCESS", str(e), file_path)
            return {"success": False, "message": f"Error processing file: {str(e)}"}
    
    def extract_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            reader = PdfReader(file_path)
            text = ""
            
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            logger.log_action("extract_pdf", file_path, True)
            return text.strip()
            
        except Exception as e:
            logger.log_error("PDF_EXTRACT", str(e), file_path)
            return None
    
    def extract_from_text(self, file_path):
        """Extract text from text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                text = f.read()
            
            logger.log_action("extract_text", file_path, True)
            return text.strip()
            
        except Exception as e:
            logger.log_error("TEXT_EXTRACT", str(e), file_path)
            return None
    
    def _hash_file(self, file_path):
        """Generate hash of file for duplicate detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def _summarize_text(self, text):
        """Create AI summary of large text"""
        if not self.model:
            # Fallback: just take first N characters
            return text[:1000] + "...\n[Document too large for full storage. Gemini API not configured for summarization.]"
        
        try:
            prompt = f"""Summarize the following document concisely. Include:
1. Main topic/purpose
2. Key points (3-5 bullets)
3. Important details to remember

Document:
{text[:10000]}  

Provide a clear, useful summary in 200-300 words."""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except Exception as e:
            logger.log_error("SUMMARIZE", str(e))
            return text[:1000] + "...\n[Could not generate AI summary]"
    
    def _create_brief_summary(self, text):
        """Create brief summary for small documents"""
        if not self.model:
            # Simple fallback
            lines = text.split('\n')
            return f"Document with {len(lines)} lines, {len(text)} characters."
        
        try:
            prompt = f"""Provide a very brief 1-2 sentence summary of this document:

{text[:500]}"""
            
            response = self.model.generate_content(prompt)
            return response.text.strip()
            
        except:
            return f"Text document, {len(text)} characters."


# Global document processor instance
document_processor = DocumentProcessor()
