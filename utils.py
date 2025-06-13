import time
from functools import wraps
from typing import Callable, Any
import re

def format_file_size(size_bytes: int) -> str:
    """Convert bytes to human readable file size."""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.1f} {size_names[i]}"

def calculate_processing_time(func: Callable) -> Callable:
    """Decorator to calculate processing time of a function."""
    @wraps(func)
    def wrapper(*args, **kwargs) -> tuple:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        processing_time = end_time - start_time
        return result, processing_time
    return wrapper

def clean_text(text: str) -> str:
    """Clean and normalize text content."""
    if not text:
        return ""
    
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove control characters
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text

def extract_keywords(text: str, max_keywords: int = 10) -> list:
    """Extract keywords from text content."""
    if not text:
        return []
    
    # Convert to lowercase and extract words
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'this', 'that', 'these', 'those', 'is', 'are', 
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 
        'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 
        'must', 'can', 'its', 'his', 'her', 'their', 'our', 'your', 'him', 
        'them', 'she', 'they', 'you', 'not', 'all', 'any', 'both', 'each', 
        'few', 'more', 'most', 'other', 'some', 'such', 'only', 'own', 'same', 
        'than', 'too', 'very', 'can', 'will', 'just', 'now', 'also', 'then',
        'about', 'after', 'before', 'here', 'where', 'when', 'who', 'what',
        'how', 'why', 'which', 'through', 'during', 'into', 'from', 'up', 
        'down', 'out', 'off', 'over', 'under', 'again', 'further', 'once'
    }
    
    # Filter out stop words and short words
    keywords = [word for word in words if word not in stop_words and len(word) > 3]
    
    # Count frequency
    from collections import Counter
    word_freq = Counter(keywords)
    
    # Return most common keywords
    return [word for word, count in word_freq.most_common(max_keywords)]

def validate_file_type(filename: str, allowed_extensions: list = None) -> bool:
    """Validate if file type is allowed."""
    if allowed_extensions is None:
        allowed_extensions = ['.pdf', '.docx', '.doc']
    
    file_extension = filename.lower().split('.')[-1]
    return f'.{file_extension}' in allowed_extensions

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove/replace unsafe characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    
    # Remove control characters
    filename = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', filename)
    
    # Limit length
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1) if '.' in filename else (filename, '')
        max_name_length = 255 - len(ext) - 1
        filename = f"{name[:max_name_length]}.{ext}" if ext else name[:255]
    
    return filename

def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to specified length with suffix."""
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix

def parse_date_string(date_string: str) -> str:
    """Parse various date string formats to standardized format."""
    from datetime import datetime
    
    common_formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%S.%f',
        '%Y-%m-%dT%H:%M:%SZ',
        '%Y-%m-%d',
        '%m/%d/%Y',
        '%d/%m/%Y'
    ]
    
    for fmt in common_formats:
        try:
            parsed_date = datetime.strptime(date_string, fmt)
            return parsed_date.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            continue
    
    # If no format matches, return original string
    return date_string

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate basic similarity between two texts using word overlap."""
    if not text1 or not text2:
        return 0.0
    
    # Extract words
    words1 = set(re.findall(r'\b\w+\b', text1.lower()))
    words2 = set(re.findall(r'\b\w+\b', text2.lower()))
    
    if not words1 or not words2:
        return 0.0
    
    # Calculate Jaccard similarity
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    
    return len(intersection) / len(union) if union else 0.0

def generate_document_summary(content: str, max_sentences: int = 3) -> str:
    """Generate a basic summary of document content."""
    if not content:
        return "No content available"
    
    # Split into sentences
    sentences = re.split(r'[.!?]+', content)
    sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 10]
    
    if not sentences:
        return "No meaningful content found"
    
    # Take first few sentences as summary
    summary_sentences = sentences[:max_sentences]
    summary = '. '.join(summary_sentences)
    
    # Ensure summary ends with proper punctuation
    if not summary.endswith(('.', '!', '?')):
        summary += '.'
    
    return summary

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human readable format."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"

def get_file_type_icon(file_type: str) -> str:
    """Get appropriate icon for file type."""
    if 'pdf' in file_type.lower():
        return "📄"
    elif 'word' in file_type.lower() or 'docx' in file_type.lower():
        return "📝"
    elif 'text' in file_type.lower():
        return "📃"
    else:
        return "📋"

def validate_search_query(query: str) -> tuple:
    """Validate search query and return validation result and cleaned query."""
    if not query or not query.strip():
        return False, "Search query cannot be empty"
    
    cleaned_query = query.strip()
    
    # Check minimum length
    if len(cleaned_query) < 2:
        return False, "Search query must be at least 2 characters long"
    
    # Check maximum length
    if len(cleaned_query) > 500:
        return False, "Search query is too long (maximum 500 characters)"
    
    # Check for potentially problematic characters
    if re.search(r'[<>{}[\]\\]', cleaned_query):
        cleaned_query = re.sub(r'[<>{}[\]\\]', ' ', cleaned_query)
    
    return True, cleaned_query

def create_backup_filename(original_filename: str) -> str:
    """Create a backup filename with timestamp."""
    from datetime import datetime
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    name, ext = original_filename.rsplit('.', 1) if '.' in original_filename else (original_filename, '')
    
    if ext:
        return f"{name}_backup_{timestamp}.{ext}"
    else:
        return f"{original_filename}_backup_{timestamp}"
