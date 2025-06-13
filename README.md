# 📄 Document Analytics Platform

An advanced document processing, analysis, and intelligence system built with Python and Streamlit. This platform combines cutting-edge AI technology with an intuitive interface to revolutionize document management workflows.

## 🚀 Features

### Core Functionality
- **Smart Document Upload**: Drag & drop interface with support for PDF and Word documents
- **Web Content Scraping**: Extract and process content from websites with bulk URL processing
- **AI-Powered Classification**: Automatic categorization using machine learning with 35+ predefined categories
- **Advanced Search Engine**: Full-text search with keyword highlighting and smart filtering
- **Document Preview**: Built-in PDF viewer and text extraction for all supported formats
- **Analytics Dashboard**: Real-time statistics, performance metrics, and visual charts
- **Database Management**: Comprehensive database operations with backup and optimization tools

### Technical Features
- **Multi-format Support**: PDF, DOCX, DOC, and web content processing
- **Scalable Database**: SQLite with SQLAlchemy ORM for reliable data storage
- **Batch Processing**: Handle multiple documents and URLs simultaneously
- **Export Capabilities**: Download original files, extracted text, and analytics reports
- **Responsive Design**: Modern, mobile-friendly interface with custom styling

## 🛠️ Technology Stack

### Frontend
- **Streamlit**: Modern web application framework
- **HTML/CSS**: Custom styling and responsive design
- **JavaScript**: Enhanced user interactions

### Backend
- **Python 3.11**: Core application logic
- **SQLAlchemy**: Database ORM and management
- **SQLite**: Lightweight, reliable database engine

### AI/ML
- **Scikit-learn**: Machine learning framework
- **TF-IDF Vectorizer**: Text feature extraction
- **Naive Bayes**: Document classification algorithm

### Document Processing
- **PyPDF2**: PDF text extraction and processing
- **Python-docx**: Word document handling
- **Trafilatura**: Web content extraction and optimization

## 📋 Prerequisites

- Python 3.11 or higher
- pip package manager
- Internet connection (for web scraping features)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/rewaadawaheed/document-analytics-platform.git
cd document-analytics-platform
```

### 2. Install Dependencies
```bash
# Install required Python packages
pip install streamlit pandas numpy scikit-learn
pip install pypdf2 python-docx trafilatura
pip install sqlalchemy psycopg2-binary requests
```

### 3. Verify Installation
```bash
python -c "import streamlit; print('Streamlit installed successfully')"
```

## 🚀 Running the Application

### Start the Application
```bash
python -m  streamlit run app.py --server.port 5000
```

### Access the Platform
Open your web browser and navigate to:
```
http://localhost:5000
```

The application will automatically:
- Initialize the SQLite database
- Set up document processing components
- Load the AI classification model
- Display the home page

## 📱 Usage Guide

### 1. Home Page
- Overview of platform features and capabilities
- Quick start guide and navigation tips
- Current database statistics (if available)

### 2. Upload Documents
- **File Upload**: Select files using the file picker
- **Drag & Drop**: Simply drag files into the designated area
- **Batch Processing**: Upload multiple documents simultaneously
- **Auto-Classification**: Documents are automatically categorized

### 3. Web Scraping
- **Single URL**: Process individual web pages
- **Multiple URLs**: Enter multiple URLs (one per line)
- **Bulk Upload**: Upload a text file containing URLs
- **Content Optimization**: Extracted content is cleaned and formatted

### 4. Document Library
- View all uploaded documents in a sortable table
- Sort by title, filename, category, size, or upload date
- View detailed document information and metadata
- Delete documents when no longer needed

### 5. Search Documents
- **Full-Text Search**: Search through document content and titles
- **Keyword Highlighting**: Search terms are highlighted in results
- **Advanced Filters**: Filter by content area and case sensitivity
- **Instant Results**: Real-time search with performance metrics

### 6. Analytics Dashboard
- **Document Statistics**: Total count, size, and category distribution
- **Performance Metrics**: Processing times and efficiency scores
- **Visual Charts**: Bar charts and line graphs for data visualization
- **Export Reports**: Download comprehensive analytics reports

### 7. Document Preview
- **PDF Viewer**: Built-in PDF display with zoom and navigation
- **Text Preview**: Extracted content for all document types
- **Download Options**: Original files and extracted text
- **Metadata Display**: Document details and processing information

### 8. Database Management
- **Connection Status**: Monitor database health and performance
- **Optimization Tools**: Database cleanup and performance tuning
- **Backup Creation**: Generate database backups
- **Statistics Monitoring**: Real-time database metrics

## 🗂️ Project Structure

```
document-analytics-platform/
├── app.py                    # Main Streamlit application
├── database_manager.py       # Database operations and management
├── document_processor.py     # PDF and Word document processing
├── classifier.py            # AI document classification
├── search_engine.py         # Search functionality and highlighting
├── analytics.py             # Statistics and reporting
├── utils.py                 # Utility functions and helpers
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md                # Project documentation
└── requirements.txt         # Python dependencies (if generated)
```

## ⚙️ Configuration

### Streamlit Configuration
The application uses the following configuration (`.streamlit/config.toml`):
```toml
[server]
headless = true
address = "127.0.0.1"
port = 5000

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

### Database Configuration
- **Type**: SQLite (default)
- **File**: `documents.db` (created automatically)
- **Tables**: Documents table with full metadata support

## 🤖 AI Classification Categories

The platform supports 35+ document categories:
- Business, Technical, Legal, Medical, Academic
- Financial, Marketing, Research, Report, Scientific
- Educational, Government, News, Entertainment, Sports
- Travel, Food, Technology, Healthcare, Real Estate
- Insurance, Banking, Construction, Manufacturing, Retail
- Transportation, Energy, Environmental, Social Media
- Web Content, Blog, Tutorial, Manual, Policy, Other

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   pip install --upgrade streamlit pandas numpy
   ```

2. **Database Connection Issues**
   - Ensure write permissions in the application directory
   - Check if `documents.db` file is created
   - Restart the application

3. **PDF Processing Errors**
   ```bash
   pip install --upgrade pypdf2
   ```

4. **Web Scraping Issues**
   - Check internet connectivity
   - Verify URL accessibility
   - Some websites may block automated requests

### Performance Optimization
- For large document collections, consider regular database optimization
- Monitor memory usage with extensive web scraping operations
- Use batch processing for better performance with multiple files

## 👥 Development Team

**Computer Science Department - University Project 2024**

- **Rewaa Basem Al.Dawaheed** (ID: 20210234)
- **Israa Atef Abu Harbeed** (ID: 220200147)  
- **Nesma Moaeen Ahmed** (ID: 220213099)

## 📄 License

This project is developed as part of academic coursework. All rights reserved to the development team and the associated educational institution.

## 🔮 Future Enhancements

- PostgreSQL database support for larger deployments
- Advanced OCR capabilities for scanned documents
- Real-time collaborative features
- API endpoints for external integrations
- Enhanced machine learning models
- Multi-language document support
- Cloud storage integration

---
