import os
import sqlite3
import psycopg2
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Float, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import List, Tuple, Optional, Dict, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String(255), nullable=False)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    file_size = Column(Integer, nullable=False)
    file_type = Column(String(100), nullable=False)
    category = Column(String(100))
    upload_date = Column(DateTime, default=datetime.utcnow)
    processing_time = Column(Float)
    file_data = Column(LargeBinary)
    
    def to_tuple(self):
        """Convert to tuple format for backward compatibility"""
        return (
            self.id, self.filename, self.title, self.content, 
            self.file_size, self.file_type, self.category, 
            self.upload_date.isoformat() if self.upload_date else None,
            self.processing_time, self.file_data
        )

class DatabaseManager:
    def __init__(self, use_postgresql: bool = True):
        """Initialize database manager with PostgreSQL or SQLite"""
        self.use_postgresql = use_postgresql
        self.engine = None
        self.Session = None
        self.session = None
        
        self._setup_database()
    
    def _setup_database(self):
        """Setup database connection and create tables"""
        try:
            # Always use SQLite for better stability
            logger.info("Using SQLite database")
            self.engine = create_engine('sqlite:///documents.db', echo=False)
            self.use_postgresql = False
            
            # Create tables
            Base.metadata.create_all(self.engine)
            
            # Create session
            self.Session = sessionmaker(bind=self.engine)
            self.session = self.Session()
            
            logger.info("Database setup complete using SQLite")
            
        except Exception as e:
            logger.error(f"Database setup failed: {str(e)}")
            raise
    
    def add_document(self, filename: str, title: str, content: str, 
                    file_data: bytes, file_size: int, file_type: str, 
                    category: str = None, processing_time: float = None) -> int:
        """Add a new document to the database"""
        try:
            document = Document(
                filename=filename,
                title=title,
                content=content,
                file_data=file_data,
                file_size=file_size,
                file_type=file_type,
                category=category,
                processing_time=processing_time
            )
            
            self.session.add(document)
            self.session.commit()
            
            logger.info(f"Document added with ID: {document.id}")
            return document.id
            
        except Exception as e:
            logger.error(f"Error adding document: {str(e)}")
            self.session.rollback()
            raise
    
    def get_document(self, doc_id: int) -> Optional[Tuple]:
        """Get a document by ID"""
        try:
            document = self.session.query(Document).filter(Document.id == doc_id).first()
            return document.to_tuple() if document else None
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {str(e)}")
            return None
    
    def get_all_documents(self) -> List[Tuple]:
        """Get all documents from the database"""
        try:
            documents = self.session.query(Document).order_by(Document.upload_date.desc()).all()
            return [doc.to_tuple() for doc in documents]
        except Exception as e:
            logger.error(f"Error getting all documents: {str(e)}")
            return []
    
    def search_documents(self, query: str, search_field: str = 'content') -> List[Tuple]:
        """Search documents by content or title"""
        try:
            if search_field == 'content':
                documents = self.session.query(Document).filter(
                    Document.content.contains(query)
                ).order_by(Document.upload_date.desc()).all()
            elif search_field == 'title':
                documents = self.session.query(Document).filter(
                    Document.title.contains(query)
                ).order_by(Document.upload_date.desc()).all()
            else:  # search both
                documents = self.session.query(Document).filter(
                    (Document.content.contains(query)) | (Document.title.contains(query))
                ).order_by(Document.upload_date.desc()).all()
            
            return [doc.to_tuple() for doc in documents]
        except Exception as e:
            logger.error(f"Error searching documents: {str(e)}")
            return []
    
    def update_document_category(self, doc_id: int, category: str):
        """Update the category of a document"""
        try:
            document = self.session.query(Document).filter(Document.id == doc_id).first()
            if document:
                document.category = category
                self.session.commit()
                logger.info(f"Updated category for document {doc_id}")
        except Exception as e:
            logger.error(f"Error updating document category: {str(e)}")
            self.session.rollback()
    
    def delete_document(self, doc_id: int) -> bool:
        """Delete a document from the database"""
        try:
            document = self.session.query(Document).filter(Document.id == doc_id).first()
            if document:
                self.session.delete(document)
                self.session.commit()
                logger.info(f"Deleted document {doc_id}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting document: {str(e)}")
            self.session.rollback()
            return False
    
    def get_documents_by_category(self, category: str) -> List[Tuple]:
        """Get all documents in a specific category"""
        try:
            documents = self.session.query(Document).filter(
                Document.category == category
            ).order_by(Document.upload_date.desc()).all()
            return [doc.to_tuple() for doc in documents]
        except Exception as e:
            logger.error(f"Error getting documents by category: {str(e)}")
            return []
    
    def get_categories(self) -> List[str]:
        """Get all unique categories"""
        try:
            categories = self.session.query(Document.category).distinct().filter(
                Document.category.isnot(None)
            ).all()
            return [cat[0] for cat in categories if cat[0]]
        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}")
            return []
    
    def get_database_stats(self) -> Dict[str, Any]:
        """Get comprehensive database statistics"""
        try:
            total_docs = self.session.query(Document).count()
            
            # Total size
            total_size_result = self.session.query(
                self.session.query(Document.file_size).filter(
                    Document.file_size.isnot(None)
                ).subquery().c.file_size.sum()
            ).scalar()
            total_size = total_size_result or 0
            
            # Average processing time
            avg_processing_time_result = self.session.query(
                self.session.query(Document.processing_time).filter(
                    Document.processing_time.isnot(None)
                ).subquery().c.processing_time.avg()
            ).scalar()
            avg_processing_time = float(avg_processing_time_result) if avg_processing_time_result else 0
            
            # Categories count
            categories_count = self.session.query(Document.category).distinct().filter(
                Document.category.isnot(None)
            ).count()
            
            # File type distribution
            file_types = self.session.query(Document.file_type, 
                                          self.session.query(Document.id).filter(
                                              Document.file_type == Document.file_type
                                          ).count().label('count')).group_by(Document.file_type).all()
            
            return {
                'total_documents': total_docs,
                'total_size': total_size,
                'average_processing_time': avg_processing_time,
                'categories_count': categories_count,
                'file_types': {ft[0]: ft[1] for ft in file_types},
                'database_type': 'PostgreSQL' if self.use_postgresql else 'SQLite'
            }
        except Exception as e:
            logger.error(f"Error getting database stats: {str(e)}")
            return {
                'total_documents': 0,
                'total_size': 0,
                'average_processing_time': 0,
                'categories_count': 0,
                'file_types': {},
                'database_type': 'PostgreSQL' if self.use_postgresql else 'SQLite'
            }
    
    def backup_database(self) -> str:
        """Create a backup of the database"""
        try:
            if self.use_postgresql:
                return "PostgreSQL backup should be handled by database administrator"
            else:
                import shutil
                backup_filename = f"documents_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                shutil.copy2('documents.db', backup_filename)
                return f"Backup created: {backup_filename}"
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            return f"Backup failed: {str(e)}"
    
    def optimize_database(self):
        """Optimize database performance"""
        try:
            if self.use_postgresql:
                # PostgreSQL optimization
                self.session.execute("VACUUM ANALYZE;")
                self.session.commit()
                logger.info("PostgreSQL database optimized")
            else:
                # SQLite optimization
                self.session.execute("VACUUM;")
                self.session.execute("ANALYZE;")
                self.session.commit()
                logger.info("SQLite database optimized")
        except Exception as e:
            logger.error(f"Error optimizing database: {str(e)}")
            self.session.rollback()
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database connection and configuration information"""
        try:
            info = {
                'database_type': 'PostgreSQL' if self.use_postgresql else 'SQLite',
                'connection_status': 'Connected' if self.session else 'Disconnected',
                'total_documents': self.session.query(Document).count(),
            }
            
            if self.use_postgresql:
                info.update({
                    'host': os.getenv('PGHOST', 'localhost'),
                    'port': os.getenv('PGPORT', '5432'),
                    'database': os.getenv('PGDATABASE', 'documents'),
                    'user': os.getenv('PGUSER', 'user')
                })
            else:
                info.update({
                    'database_file': 'documents.db',
                    'file_size': os.path.getsize('documents.db') if os.path.exists('documents.db') else 0
                })
            
            return info
        except Exception as e:
            logger.error(f"Error getting database info: {str(e)}")
            return {'error': str(e)}
    
    def close(self):
        """Close database connection"""
        try:
            if self.session:
                self.session.close()
                logger.info("Database connection closed")
        except Exception as e:
            logger.error(f"Error closing database: {str(e)}")
    
    def __del__(self):
        """Cleanup when object is destroyed"""
        self.close()