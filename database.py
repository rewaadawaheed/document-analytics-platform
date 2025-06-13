import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

class DocumentDatabase:
    def __init__(self, db_path: str = "documents.db"):
        """Initialize the document database."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the documents table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                file_size INTEGER NOT NULL,
                file_type TEXT NOT NULL,
                category TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                processing_time REAL,
                file_data BLOB
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_document(self, filename: str, title: str, content: str, 
                    file_data: bytes, file_size: int, file_type: str, 
                    category: str = None, processing_time: float = None) -> int:
        """Add a new document to the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO documents 
            (filename, title, content, file_size, file_type, category, processing_time, file_data)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (filename, title, content, file_size, file_type, category, processing_time, file_data))
        
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return doc_id
    
    def get_document(self, doc_id: int) -> Optional[Tuple]:
        """Get a document by ID."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM documents WHERE id = ?', (doc_id,))
        document = cursor.fetchone()
        
        conn.close()
        return document
    
    def get_all_documents(self) -> List[Tuple]:
        """Get all documents from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM documents ORDER BY upload_date DESC')
        documents = cursor.fetchall()
        
        conn.close()
        return documents
    
    def search_documents(self, query: str, search_field: str = 'content') -> List[Tuple]:
        """Search documents by content or title."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if search_field == 'content':
            cursor.execute(
                'SELECT * FROM documents WHERE content LIKE ? ORDER BY upload_date DESC',
                (f'%{query}%',)
            )
        elif search_field == 'title':
            cursor.execute(
                'SELECT * FROM documents WHERE title LIKE ? ORDER BY upload_date DESC',
                (f'%{query}%',)
            )
        else:  # search both
            cursor.execute(
                'SELECT * FROM documents WHERE content LIKE ? OR title LIKE ? ORDER BY upload_date DESC',
                (f'%{query}%', f'%{query}%')
            )
        
        documents = cursor.fetchall()
        conn.close()
        return documents
    
    def update_document_category(self, doc_id: int, category: str):
        """Update the category of a document."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'UPDATE documents SET category = ? WHERE id = ?',
            (category, doc_id)
        )
        
        conn.commit()
        conn.close()
    
    def delete_document(self, doc_id: int) -> bool:
        """Delete a document from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM documents WHERE id = ?', (doc_id,))
        success = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        return success
    
    def get_documents_by_category(self, category: str) -> List[Tuple]:
        """Get all documents in a specific category."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT * FROM documents WHERE category = ? ORDER BY upload_date DESC',
            (category,)
        )
        documents = cursor.fetchall()
        
        conn.close()
        return documents
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT category FROM documents WHERE category IS NOT NULL')
        categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return categories
    
    def get_database_stats(self) -> dict:
        """Get basic database statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Total documents
        cursor.execute('SELECT COUNT(*) FROM documents')
        total_docs = cursor.fetchone()[0]
        
        # Total size
        cursor.execute('SELECT SUM(file_size) FROM documents')
        total_size = cursor.fetchone()[0] or 0
        
        # Average processing time
        cursor.execute('SELECT AVG(processing_time) FROM documents WHERE processing_time IS NOT NULL')
        avg_processing_time = cursor.fetchone()[0] or 0
        
        # Categories count
        cursor.execute('SELECT COUNT(DISTINCT category) FROM documents WHERE category IS NOT NULL')
        categories_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'total_documents': total_docs,
            'total_size': total_size,
            'average_processing_time': avg_processing_time,
            'categories_count': categories_count
        }
