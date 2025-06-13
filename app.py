import streamlit as st
import os
import time
import base64
from datetime import datetime
import pandas as pd
import trafilatura
import requests
from database_manager import DatabaseManager
from document_processor import DocumentProcessor
from classifier import DocumentClassifier
from search_engine import SearchEngine
from analytics import Analytics
from utils import format_file_size, calculate_processing_time

# Initialize components
@st.cache_resource
def init_components():
    db = DatabaseManager()
    processor = DocumentProcessor()
    classifier = DocumentClassifier()
    search_engine = SearchEngine()
    analytics = Analytics()
    return db, processor, classifier, search_engine, analytics

def main():
    st.set_page_config(
        page_title="Document Analytics Platform",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for styling
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    .stSelectbox > div > div > select {
        background-color: #f8f9fa;
        border: 2px solid #667eea;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize components
    db, processor, classifier, search_engine, analytics = init_components()
    
    # Sidebar for navigation with custom styling
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin-bottom: 1rem;">
        <h2 style="color: white; margin: 0;">📄 DocAnalytics</h2>
        <p style="color: #e0e0e0; margin: 0; font-size: 0.9em;">Navigation</p>
    </div>
    """, unsafe_allow_html=True)
    page = st.sidebar.selectbox(
        "Choose a page",
        ["🏠 Home", "📤 Upload Documents", "🌐 Web Scraping", "📚 Document Library", "🔍 Search Documents", "📊 Analytics Dashboard", "👁️ Document Preview", "🗄️ Database Management"]
    )
    
    if page == "🏠 Home":
        home_page()
    elif page == "📤 Upload Documents":
        upload_page(db, processor, classifier)
    elif page == "🌐 Web Scraping":
        web_scraping_page(db, processor, classifier)
    elif page == "📚 Document Library":
        library_page(db)
    elif page == "🔍 Search Documents":
        search_page(db, search_engine)
    elif page == "📊 Analytics Dashboard":
        analytics_page(db, analytics)
    elif page == "👁️ Document Preview":
        preview_page(db)
    elif page == "🗄️ Database Management":
        database_management_page(db)
    
    # Add developer info to sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px; margin-top: 2rem;">
        <h4 style="color: #333; margin-bottom: 0.5rem;">👥 Development Team</h4>
        <p style="color: #666; font-size: 0.9em; margin: 0.2rem 0;"><strong>Rewaa Basem Al.Dawaheed</strong><br>ID: 20210234</p>
        <p style="color: #666; font-size: 0.9em; margin: 0.2rem 0;"><strong>Israa Atef Abu Harbeed</strong><br>ID: 220200147</p>  
        <p style="color: #666; font-size: 0.9em; margin: 0.2rem 0;"><strong>Nesma Moaeen Ahmed</strong><br>ID: 220213099</p>
        <p style="color: #888; font-size: 0.8em; margin-top: 0.5rem;">This project was undertaken in partial fulfillment of the requirements for the course <b>Cloud and Distributed Systems (SICT 4313)</b> at the Islamic University of Gaza, under the guidance of <b>Dr. Rebhi S. Baraka</b>.</p>
    </div>
    """, unsafe_allow_html=True)

def home_page():
    # Hero Section
    st.markdown("""
    <div class="main-header">
        <h1 style="margin: 0; font-size: 3rem;">📄 Document Analytics Platform</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">
            Advanced Document Processing, Analysis & Intelligence System
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Welcome Message
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h2 style="color: #333;">Welcome to the Future of Document Management</h2>
        <p style="color: #666; font-size: 1.1rem; max-width: 800px; margin: 0 auto;">
            Our platform combines cutting-edge AI technology with intuitive design to revolutionize how you 
            process, analyze, and manage your document collections. From automated classification to advanced 
            search capabilities, we've got your document workflow covered.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Key Features
    st.subheader("🚀 Key Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h4>📤 Smart Upload</h4>
            <ul>
                <li>Drag & drop interface</li>
                <li>PDF and Word support</li>
                <li>Batch processing</li>
                <li>Auto-classification</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>🔍 Advanced Search</h4>
            <ul>
                <li>Full-text search</li>
                <li>Keyword highlighting</li>
                <li>Smart filters</li>
                <li>Instant results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h4>🌐 Web Scraping</h4>
            <ul>
                <li>Extract from websites</li>
                <li>Bulk URL processing</li>
                <li>Content optimization</li>
                <li>Auto-categorization</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>📊 Analytics Dashboard</h4>
            <ul>
                <li>Real-time statistics</li>
                <li>Performance metrics</li>
                <li>Visual charts</li>
                <li>Export reports</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h4>🤖 AI Classification</h4>
            <ul>
                <li>35+ categories</li>
                <li>Machine learning</li>
                <li>Auto-tagging</li>
                <li>High accuracy</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h4>👁️ Document Preview</h4>
            <ul>
                <li>PDF viewer</li>
                <li>Text extraction</li>
                <li>Download options</li>
                <li>Metadata display</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Technology Stack
    st.subheader("🛠️ Technology Stack")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <h4>Frontend</h4>
            <p>Streamlit<br>HTML/CSS<br>JavaScript</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <h4>Backend</h4>
            <p>Python<br>SQLAlchemy<br>SQLite</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <h4>AI/ML</h4>
            <p>Scikit-learn<br>TF-IDF<br>Naive Bayes</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <h4>Processing</h4>
            <p>PyPDF2<br>Python-docx<br>Trafilatura</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Getting Started
    st.subheader("🎯 Getting Started")
    
    st.markdown("""
    <div style="background: #e3f2fd; padding: 2rem; border-radius: 10px; border-left: 5px solid #2196f3;">
        <h4 style="color: #1976d2; margin-top: 0;">Quick Start Guide</h4>
        <ol style="color: #333; line-height: 1.8;">
            <li><strong>Upload Documents:</strong> Use the drag & drop interface to upload your PDF or Word files</li>
            <li><strong>Web Scraping:</strong> Extract content from websites using single or bulk URL processing</li>
            <li><strong>Search & Analyze:</strong> Use the powerful search engine to find specific content</li>
            <li><strong>View Analytics:</strong> Monitor your document collection with comprehensive statistics</li>
            <li><strong>Preview & Download:</strong> View documents directly in the browser or download them</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    # Statistics Preview (if available)
    try:
        from database_manager import DatabaseManager
        db = DatabaseManager()
        stats = db.get_database_stats()
        
        if stats.get('total_documents', 0) > 0:
            st.subheader("📈 Current Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Documents", stats.get('total_documents', 0))
            with col2:
                from utils import format_file_size
                st.metric("Total Size", format_file_size(stats.get('total_size', 0)))
            with col3:
                st.metric("Categories", stats.get('categories_count', 0))
            with col4:
                st.metric("Database", stats.get('database_type', 'SQLite'))
    except:
        pass
    
    # Call to Action
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; margin: 2rem 0;">
        <h3 style="color: white; margin-bottom: 1rem;">Ready to Get Started?</h3>
        <p style="color: #e0e0e0; margin-bottom: 1.5rem;">Choose from the navigation menu to begin processing your documents!</p>
    </div>
    """, unsafe_allow_html=True)

def upload_page(db, processor, classifier):
    st.header("📤 Upload Documents")
    
    # Upload method selection
    upload_method = st.radio(
        "Choose upload method:",
        ["File Upload", "Drag & Drop"],
        horizontal=True
    )
    
    if upload_method == "File Upload":
        # File uploader
        uploaded_files = st.file_uploader(
            "Choose PDF or Word documents",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True
        )
    else:
        # Drag and drop interface
        st.info("📁 Drag and drop your files here or click to browse")
        uploaded_files = st.file_uploader(
            "Drag and drop files here",
            type=['pdf', 'docx', 'doc'],
            accept_multiple_files=True,
            label_visibility="collapsed"
        )
    
    if uploaded_files:
        st.write(f"Selected {len(uploaded_files)} file(s)")
        
        # Show file preview
        with st.expander("📋 File Preview"):
            for file in uploaded_files:
                st.write(f"• {file.name} ({format_file_size(file.size)})")
        
        if st.button("Process Documents", type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, file in enumerate(uploaded_files):
                status_text.text(f"Processing {file.name}...")
                file_path = None
                
                start_time = time.time()
                
                try:
                    # Save uploaded file temporarily
                    file_path = f"temp_{file.name}"
                    with open(file_path, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Process document
                    text_content = processor.extract_text(file_path)
                    title = processor.extract_title(text_content)
                    file_size = os.path.getsize(file_path)
                    
                    # Classify document
                    category = classifier.classify_document(text_content)
                    
                    # Calculate processing time
                    processing_time = time.time() - start_time
                    
                    # Store in database
                    with open(file_path, "rb") as f:
                        file_data = f.read()
                    
                    db.add_document(
                        filename=file.name,
                        title=title,
                        content=text_content,
                        file_data=file_data,
                        file_size=file_size,
                        file_type=file.type,
                        category=category,
                        processing_time=processing_time
                    )
                    
                    # Clean up temporary file
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                    
                    st.success(f"✅ Successfully processed: {file.name}")
                    
                except Exception as e:
                    st.error(f"❌ Error processing {file.name}: {str(e)}")
                    if file_path and os.path.exists(file_path):
                        os.remove(file_path)
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("Processing complete!")
            st.balloons()

def web_scraping_page(db, processor, classifier):
    st.header("🌐 Web Scraping")
    st.markdown("Extract content from websites and add them to your document collection")
    
    # URL input methods
    scraping_method = st.radio(
        "Choose scraping method:",
        ["Single URL", "Multiple URLs", "Bulk Upload"],
        horizontal=True
    )
    
    urls_to_scrape = []
    
    if scraping_method == "Single URL":
        url = st.text_input("Enter website URL:", placeholder="https://example.com/article")
        if url:
            urls_to_scrape = [url]
    
    elif scraping_method == "Multiple URLs":
        st.markdown("Enter URLs (one per line):")
        url_text = st.text_area("URLs:", height=150, placeholder="https://example.com/page1\nhttps://example.com/page2")
        if url_text:
            urls_to_scrape = [url.strip() for url in url_text.split('\n') if url.strip()]
    
    else:  # Bulk Upload
        uploaded_file = st.file_uploader("Upload text file with URLs (one per line)", type=['txt'])
        if uploaded_file:
            content = uploaded_file.read().decode('utf-8')
            urls_to_scrape = [url.strip() for url in content.split('\n') if url.strip()]
    
    # Display URLs to be scraped
    if urls_to_scrape:
        st.write(f"URLs to scrape: {len(urls_to_scrape)}")
        with st.expander("📋 URL Preview"):
            for i, url in enumerate(urls_to_scrape[:10], 1):
                st.write(f"{i}. {url}")
            if len(urls_to_scrape) > 10:
                st.write(f"... and {len(urls_to_scrape) - 10} more")
    
    # Scraping options
    with st.expander("⚙️ Scraping Options"):
        extract_title_from_content = st.checkbox("Extract title from content", value=True)
        classify_content = st.checkbox("Auto-classify scraped content", value=True)
        timeout_seconds = st.slider("Request timeout (seconds)", 5, 60, 15)
    
    # Start scraping
    if urls_to_scrape and st.button("🚀 Start Scraping", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        success_count = 0
        error_count = 0
        
        for i, url in enumerate(urls_to_scrape):
            status_text.text(f"Scraping: {url}")
            
            try:
                start_time = time.time()
                
                # Fetch and extract content
                downloaded = trafilatura.fetch_url(url)
                if downloaded:
                    text_content = trafilatura.extract(downloaded)
                    
                    if text_content and len(text_content.strip()) > 50:
                        # Extract or generate title
                        if extract_title_from_content:
                            title = processor.extract_title(text_content)
                        else:
                            title = f"Web Content from {url}"
                        
                        # Classify content if enabled
                        category = "Web Content"
                        if classify_content:
                            category = classifier.classify_document(text_content)
                        
                        # Calculate processing time
                        processing_time = time.time() - start_time
                        
                        # Create fake file data for web content
                        file_data = text_content.encode('utf-8')
                        file_size = len(file_data)
                        
                        # Store in database
                        filename = f"web_content_{int(time.time())}_{i+1}.txt"
                        
                        db.add_document(
                            filename=filename,
                            title=title,
                            content=text_content,
                            file_data=file_data,
                            file_size=file_size,
                            file_type="text/plain",
                            category=category,
                            processing_time=processing_time
                        )
                        
                        success_count += 1
                        st.success(f"✅ Successfully scraped: {url}")
                    else:
                        st.warning(f"⚠️ No meaningful content found: {url}")
                        error_count += 1
                else:
                    st.error(f"❌ Failed to fetch: {url}")
                    error_count += 1
                    
            except Exception as e:
                st.error(f"❌ Error scraping {url}: {str(e)}")
                error_count += 1
            
            progress_bar.progress((i + 1) / len(urls_to_scrape))
        
        status_text.text(f"Scraping complete! ✅ {success_count} successful, ❌ {error_count} failed")
        if success_count > 0:
            st.balloons()

def library_page(db):
    st.header("📚 Document Library")
    
    documents = db.get_all_documents()
    
    if not documents:
        st.info("No documents uploaded yet. Go to 'Upload Documents' to add some!")
        return
    
    # Create DataFrame for display
    df_data = []
    for doc in documents:
        df_data.append({
            'ID': doc[0],
            'Filename': doc[1],
            'Title': doc[2][:50] + "..." if len(doc[2]) > 50 else doc[2],
            'Category': doc[6],
            'Size': format_file_size(doc[4]),
            'Upload Date': doc[7]
        })
    
    df = pd.DataFrame(df_data)
    
    # Display sorting options
    col1, col2 = st.columns([1, 3])
    with col1:
        sort_by = st.selectbox("Sort by:", ["Title", "Filename", "Category", "Size", "Upload Date"])
    
    # Sort documents
    if sort_by == "Title":
        df = df.sort_values('Title')
    elif sort_by == "Filename":
        df = df.sort_values('Filename')
    elif sort_by == "Category":
        df = df.sort_values('Category')
    elif sort_by == "Size":
        # Sort by actual file size
        documents_with_size = [(doc, doc[4]) for doc in documents]
        documents_with_size.sort(key=lambda x: x[1])
        documents = [doc[0] for doc in documents_with_size]
        # Recreate DataFrame
        df_data = []
        for doc in documents:
            df_data.append({
                'ID': doc[0],
                'Filename': doc[1],
                'Title': doc[2][:50] + "..." if len(doc[2]) > 50 else doc[2],
                'Category': doc[6],
                'Size': format_file_size(doc[4]),
                'Upload Date': doc[7]
            })
        df = pd.DataFrame(df_data)
    elif sort_by == "Upload Date":
        df = df.sort_values('Upload Date')
    
    # Display documents
    st.dataframe(df, use_container_width=True)
    
    # Document details
    st.subheader("Document Details")
    selected_id = st.selectbox("Select document to view details:", 
                              options=[doc[0] for doc in documents],
                              format_func=lambda x: next(doc[1] for doc in documents if doc[0] == x))
    
    if selected_id:
        doc = db.get_document(selected_id)
        if doc:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Filename:** {doc[1]}")
                st.write(f"**Title:** {doc[2]}")
                st.write(f"**Category:** {doc[6]}")
            with col2:
                st.write(f"**File Size:** {format_file_size(doc[4])}")
                st.write(f"**Upload Date:** {doc[7]}")
                st.write(f"**Processing Time:** {doc[8]:.2f}s")
            
            # Show content preview
            st.subheader("Content Preview")
            content_preview = doc[3][:500] + "..." if len(doc[3]) > 500 else doc[3]
            st.text_area("Document Content", content_preview, height=200, disabled=True)
            
            # Delete button
            if st.button(f"Delete Document", type="secondary"):
                db.delete_document(selected_id)
                st.success("Document deleted successfully!")
                st.rerun()

def search_page(db, search_engine):
    st.header("🔍 Search Documents")
    
    documents = db.get_all_documents()
    
    if not documents:
        st.info("No documents available for search. Upload some documents first!")
        return
    
    # Search interface
    search_query = st.text_input("Enter search terms:")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        search_in = st.selectbox("Search in:", ["Content", "Title", "Both"])
    with col2:
        case_sensitive = st.checkbox("Case sensitive")
    
    if search_query and st.button("Search", type="primary"):
        start_time = time.time()
        
        results = search_engine.search_documents(
            documents, search_query, search_in, case_sensitive
        )
        
        search_time = time.time() - start_time
        
        st.write(f"Found {len(results)} result(s) in {search_time:.3f} seconds")
        
        if results:
            for doc_id, doc_data, highlighted_content in results:
                with st.expander(f"📄 {doc_data[1]} - {doc_data[2][:50]}..."):
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.write(f"**Category:** {doc_data[6]}")
                        st.write(f"**File Size:** {format_file_size(doc_data[4])}")
                    with col2:
                        if st.button(f"View Full Document", key=f"view_{doc_id}"):
                            st.session_state['preview_doc_id'] = doc_id
                            st.rerun()
                    
                    st.subheader("Highlighted Content")
                    st.markdown(highlighted_content, unsafe_allow_html=True)
        else:
            st.info("No documents found matching your search criteria.")

def analytics_page(db, analytics):
    st.header("📊 Analytics Dashboard")
    
    documents = db.get_all_documents()
    
    if not documents:
        st.info("No documents available for analytics. Upload some documents first!")
        return
    
    # Generate analytics
    stats = analytics.generate_statistics(documents)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", stats['total_documents'])
    with col2:
        st.metric("Total Size", format_file_size(stats['total_size']))
    with col3:
        st.metric("Avg Processing Time", f"{stats['avg_processing_time']:.2f}s")
    with col4:
        st.metric("Categories", len(stats['categories']))
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Documents by Category")
        if stats['categories']:
            category_data = list(stats['categories'].items())
            category_df = pd.DataFrame(category_data, columns=['Category', 'Count'])
            st.bar_chart(category_df.set_index('Category')['Count'])
        else:
            st.info("No categorized documents yet.")
    
    with col2:
        st.subheader("File Size Distribution")
        if documents:
            size_data = [doc[4] for doc in documents]
            size_df = pd.DataFrame({'File Size (MB)': [s/1024/1024 for s in size_data]})
            st.line_chart(size_df)
    
    # Performance metrics
    st.subheader("Performance Metrics")
    
    processing_times = [doc[8] for doc in documents if doc[8]]
    if processing_times:
        perf_col1, perf_col2, perf_col3 = st.columns(3)
        
        with perf_col1:
            st.metric("Min Processing Time", f"{min(processing_times):.2f}s")
        with perf_col2:
            st.metric("Max Processing Time", f"{max(processing_times):.2f}s")
        with perf_col3:
            st.metric("Total Processing Time", f"{sum(processing_times):.2f}s")
        
        # Processing time chart
        time_df = pd.DataFrame({'Processing Time (s)': processing_times})
        st.line_chart(time_df)
    
    # Detailed statistics table
    st.subheader("Document Statistics")
    if documents:
        detailed_stats = []
        for doc in documents:
            detailed_stats.append({
                'Filename': doc[1],
                'Title': doc[2][:30] + "..." if len(doc[2]) > 30 else doc[2],
                'Category': doc[6],
                'Size': format_file_size(doc[4]),
                'Processing Time': f"{doc[8]:.2f}s" if doc[8] else "N/A",
                'Upload Date': doc[7]
            })
        
        stats_df = pd.DataFrame(detailed_stats)
        st.dataframe(stats_df, use_container_width=True)

def preview_page(db):
    st.header("👁️ Document Preview")
    
    documents = db.get_all_documents()
    
    if not documents:
        st.info("No documents available for preview. Upload some documents first!")
        return
    
    # Filter documents by type
    preview_filter = st.radio(
        "Filter by document type:",
        ["All Documents", "PDF Documents", "Word Documents", "Web Content"],
        horizontal=True
    )
    
    filtered_documents = documents
    if preview_filter == "PDF Documents":
        filtered_documents = [doc for doc in documents if 'pdf' in doc[5].lower()]
    elif preview_filter == "Word Documents":
        filtered_documents = [doc for doc in documents if 'word' in doc[5].lower() or 'docx' in doc[5].lower()]
    elif preview_filter == "Web Content":
        filtered_documents = [doc for doc in documents if 'text' in doc[5].lower()]
    
    if not filtered_documents:
        st.info(f"No {preview_filter.lower()} available for preview.")
        return
    
    # Document selector
    if 'preview_doc_id' in st.session_state:
        default_index = next((i for i, doc in enumerate(filtered_documents) 
                            if doc[0] == st.session_state['preview_doc_id']), 0)
    else:
        default_index = 0
    
    selected_doc = st.selectbox(
        "Select document:",
        options=filtered_documents,
        format_func=lambda x: f"{x[1]} - {x[2][:50]}...",
        index=default_index
    )
    
    if selected_doc:
        doc_id = selected_doc[0]
        doc_data = db.get_document(doc_id)
        
        if doc_data:
            # Display document info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.write(f"**Filename:** {doc_data[1]}")
            with col2:
                st.write(f"**Type:** {doc_data[5]}")
            with col3:
                st.write(f"**Size:** {format_file_size(doc_data[4])}")
            with col4:
                st.write(f"**Category:** {doc_data[6]}")
            
            # Document Preview based on type
            file_type = doc_data[5].lower()
            
            if 'pdf' in file_type and doc_data[9]:
                st.subheader("📄 PDF Preview")
                try:
                    # Convert PDF bytes to base64 for display
                    pdf_base64 = base64.b64encode(doc_data[9]).decode('utf-8')
                    
                    # Create PDF viewer using iframe
                    pdf_display = f"""
                    <iframe 
                        src="data:application/pdf;base64,{pdf_base64}" 
                        width="100%" 
                        height="800px" 
                        type="application/pdf">
                        <p>Your browser does not support PDF preview. 
                        <a href="data:application/pdf;base64,{pdf_base64}" download="{doc_data[1]}">
                        Download the PDF</a> to view it.</p>
                    </iframe>
                    """
                    
                    st.markdown(pdf_display, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error displaying PDF: {str(e)}")
                    st.info("PDF preview not available, showing text content instead.")
                    st.text_area("Document Content", doc_data[3], height=400, disabled=True)
            
            elif 'word' in file_type or 'docx' in file_type:
                st.subheader("📝 Word Document Preview")
                st.info("Word documents are displayed as extracted text content")
                st.text_area("Document Content", doc_data[3], height=600, disabled=True)
            
            elif 'text' in file_type:
                st.subheader("📃 Text Content Preview")
                st.text_area("Document Content", doc_data[3], height=600, disabled=True)
            
            else:
                st.subheader("📋 Document Content")
                st.info("Preview showing extracted text content")
                st.text_area("Document Content", doc_data[3], height=600, disabled=True)
            
            # Additional document details
            with st.expander("📊 Document Details"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Document ID:** {doc_data[0]}")
                    st.write(f"**Upload Date:** {doc_data[7]}")
                    st.write(f"**Processing Time:** {doc_data[8]:.2f}s" if doc_data[8] else "N/A")
                with col2:
                    st.write(f"**Content Length:** {len(doc_data[3])} characters")
                    st.write(f"**Word Count:** {len(doc_data[3].split())} words")
                    st.write(f"**Title Length:** {len(doc_data[2])} characters")
            
            # Download options
            st.subheader("📥 Download Options")
            col1, col2 = st.columns(2)
            
            with col1:
                if doc_data[9]:  # If file data exists
                    st.download_button(
                        label=f"Download Original File",
                        data=doc_data[9],
                        file_name=doc_data[1],
                        mime=doc_data[5]
                    )
            
            with col2:
                # Download as text
                st.download_button(
                    label="Download as Text",
                    data=doc_data[3],
                    file_name=f"{doc_data[1].split('.')[0]}_content.txt",
                    mime="text/plain"
                )
                
        else:
            st.error("Document data not found.")

def database_management_page(db):
    st.header("🗄️ Database Management")
    st.markdown("Manage your document database, view statistics, and perform maintenance operations")
    
    # Database Information
    st.subheader("📊 Database Information")
    
    try:
        db_info = db.get_database_info()
        db_stats = db.get_database_stats()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Database Type", db_stats.get('database_type', 'Unknown'))
        with col2:
            st.metric("Total Documents", db_stats.get('total_documents', 0))
        with col3:
            st.metric("Total Size", format_file_size(db_stats.get('total_size', 0)))
        with col4:
            st.metric("Categories", db_stats.get('categories_count', 0))
        
        # Connection Details
        with st.expander("🔌 Connection Details"):
            if db_stats.get('database_type') == 'PostgreSQL':
                st.write(f"**Host:** {db_info.get('host', 'N/A')}")
                st.write(f"**Port:** {db_info.get('port', 'N/A')}")
                st.write(f"**Database:** {db_info.get('database', 'N/A')}")
                st.write(f"**User:** {db_info.get('user', 'N/A')}")
                st.write(f"**Status:** {db_info.get('connection_status', 'Unknown')}")
            else:
                st.write(f"**File:** {db_info.get('database_file', 'N/A')}")
                st.write(f"**File Size:** {format_file_size(db_info.get('file_size', 0))}")
                st.write(f"**Status:** {db_info.get('connection_status', 'Unknown')}")
        
        # Database Statistics
        st.subheader("📈 Database Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Performance Metrics:**")
            avg_processing = db_stats.get('average_processing_time', 0)
            st.write(f"• Average Processing Time: {avg_processing:.2f}s")
            
            if db_stats.get('file_types'):
                st.write("**File Type Distribution:**")
                for file_type, count in db_stats['file_types'].items():
                    st.write(f"• {file_type}: {count} documents")
        
        with col2:
            if db_stats.get('file_types'):
                st.write("**File Type Chart:**")
                file_type_data = list(db_stats['file_types'].items())
                if file_type_data:
                    file_type_df = pd.DataFrame(file_type_data, columns=['Type', 'Count'])
                    st.bar_chart(file_type_df.set_index('Type')['Count'])
        
        # Database Operations
        st.subheader("🔧 Database Operations")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔄 Optimize Database", help="Optimize database performance"):
                with st.spinner("Optimizing database..."):
                    try:
                        db.optimize_database()
                        st.success("Database optimized successfully!")
                    except Exception as e:
                        st.error(f"Optimization failed: {str(e)}")
        
        with col2:
            if st.button("💾 Create Backup", help="Create database backup"):
                with st.spinner("Creating backup..."):
                    try:
                        backup_result = db.backup_database()
                        st.success(backup_result)
                    except Exception as e:
                        st.error(f"Backup failed: {str(e)}")
        
        with col3:
            if st.button("🔍 Test Connection", help="Test database connection"):
                try:
                    test_docs = db.get_all_documents()
                    st.success(f"Connection successful! Found {len(test_docs)} documents.")
                except Exception as e:
                    st.error(f"Connection test failed: {str(e)}")
        
        # Maintenance Section
        st.subheader("🧹 Maintenance")
        
        with st.expander("⚠️ Advanced Operations"):
            st.warning("These operations can affect your data. Use with caution.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Cleanup Operations:**")
                if st.button("🗑️ Remove Orphaned Records", help="Remove records without file data"):
                    st.info("This feature is not yet implemented")
                
                if st.button("📊 Rebuild Statistics", help="Rebuild database statistics"):
                    with st.spinner("Rebuilding statistics..."):
                        try:
                            db.optimize_database()
                            st.success("Statistics rebuilt successfully!")
                        except Exception as e:
                            st.error(f"Failed to rebuild statistics: {str(e)}")
            
            with col2:
                st.write("**Data Export:**")
                if st.button("📤 Export All Data", help="Export all documents as JSON"):
                    st.info("This feature is not yet implemented")
                
                if st.button("📊 Generate Report", help="Generate comprehensive database report"):
                    try:
                        documents = db.get_all_documents()
                        analytics = Analytics()
                        report = analytics.export_analytics_report(documents)
                        
                        st.download_button(
                            label="Download Database Report",
                            data=report,
                            file_name=f"database_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                            mime="text/plain"
                        )
                        st.success("Report generated successfully!")
                    except Exception as e:
                        st.error(f"Report generation failed: {str(e)}")
        
        # Recent Activity
        st.subheader("📋 Recent Activity")
        try:
            recent_docs = db.get_all_documents()[:10]  # Get last 10 documents
            if recent_docs:
                recent_data = []
                for doc in recent_docs:
                    recent_data.append({
                        'ID': doc[0],
                        'Filename': doc[1][:30] + "..." if len(doc[1]) > 30 else doc[1],
                        'Category': doc[6] or 'Uncategorized',
                        'Size': format_file_size(doc[4]),
                        'Upload Date': doc[7]
                    })
                
                recent_df = pd.DataFrame(recent_data)
                st.dataframe(recent_df, use_container_width=True)
            else:
                st.info("No recent activity found.")
        except Exception as e:
            st.error(f"Error loading recent activity: {str(e)}")
            
    except Exception as e:
        st.error(f"Error loading database information: {str(e)}")
        st.info("The database might not be properly initialized. Try uploading a document first.")

if __name__ == "__main__":
    main()
