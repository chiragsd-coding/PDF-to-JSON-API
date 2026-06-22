import pdfplumber
import json
import os
from typing import Dict, Any, List
from datetime import datetime

class PDFProcessor:
    """Handles PDF to JSON conversion."""
    
    @staticmethod
    def extract_text(pdf_path: str) -> Dict[str, Any]:
        """Extract text content from PDF file."""
        pages_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_data = {
                    "page_number": page_num,
                    "text": page.extract_text() or "",
                    "width": page.width,
                    "height": page.height
                }
                pages_data.append(page_data)
        
        return {
            "pages": pages_data,
            "total_pages": len(pages_data),
            "extracted_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def extract_tables(pdf_path: str) -> Dict[str, Any]:
        """Extract tables from PDF file."""
        tables_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_tables = page.extract_tables()
                if page_tables:
                    for table_num, table in enumerate(page_tables, 1):
                        # Convert table to list of dictionaries
                        headers = table[0] if table else []
                        table_rows = []
                        for row in table[1:]:
                            row_dict = {}
                            for i, header in enumerate(headers):
                                if i < len(row):
                                    row_dict[header] = row[i]
                            table_rows.append(row_dict)
                        
                        tables_data.append({
                            "page_number": page_num,
                            "table_number": table_num,
                            "headers": headers,
                            "rows": table_rows
                        })
        
        return {
            "tables": tables_data,
            "total_tables": len(tables_data),
            "extracted_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def extract_images(pdf_path: str) -> Dict[str, Any]:
        """Extract images from PDF file."""
        images_data = []
        
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                page_images = page.images
                if page_images:
                    for img_num, img in enumerate(page_images, 1):
                        images_data.append({
                            "page_number": page_num,
                            "image_number": img_num,
                            "x0": img.get("x0", 0),
                            "y0": img.get("y0", 0),
                            "x1": img.get("x1", 0),
                            "y1": img.get("y1", 0),
                            "width": img.get("width", 0),
                            "height": img.get("height", 0)
                        })
        
        return {
            "images": images_data,
            "total_images": len(images_data),
            "extracted_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def extract_metadata(pdf_path: str) -> Dict[str, Any]:
        """Extract PDF metadata."""
        with pdfplumber.open(pdf_path) as pdf:
            metadata = pdf.metadata or {}
            metadata["total_pages"] = len(pdf.pages)
            return metadata
    
    @classmethod
    def process_pdf(cls, pdf_path: str) -> Dict[str, Any]:
        """Process PDF and return complete structured JSON."""
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        result = {
            "metadata": cls.extract_metadata(pdf_path),
            "text_content": cls.extract_text(pdf_path),
            "tables": cls.extract_tables(pdf_path),
            "images": cls.extract_images(pdf_path),
            "processed_at": datetime.utcnow().isoformat()
        }
        
        return result
