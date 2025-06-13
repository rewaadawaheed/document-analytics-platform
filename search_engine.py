import re
from typing import List, Tuple

class SearchEngine:
    def __init__(self):
        """Initialize the search engine."""
        pass
    
    def search_documents(self, documents: List[tuple], query: str, 
                        search_in: str = "Content", case_sensitive: bool = False) -> List[Tuple]:
        """
        Search documents for a given query.
        
        Args:
            documents: List of document tuples from database
            query: Search query string
            search_in: Where to search ("Content", "Title", "Both")
            case_sensitive: Whether search should be case sensitive
        
        Returns:
            List of tuples: (doc_id, document_data, highlighted_content)
        """
        if not query.strip():
            return []
        
        results = []
        search_terms = self._parse_query(query)
        
        for doc in documents:
            doc_id = doc[0]
            title = doc[2]
            content = doc[3]
            
            # Determine search text based on search_in parameter
            if search_in == "Title":
                search_text = title
            elif search_in == "Content":
                search_text = content
            else:  # "Both"
                search_text = f"{title} {content}"
            
            # Check if document matches query
            if self._document_matches(search_text, search_terms, case_sensitive):
                # Generate highlighted content for display
                highlighted_content = self._highlight_matches(
                    content, search_terms, case_sensitive
                )
                results.append((doc_id, doc, highlighted_content))
        
        return results
    
    def _parse_query(self, query: str) -> List[str]:
        """Parse search query into individual terms."""
        # Handle quoted phrases
        quoted_phrases = re.findall(r'"([^"]*)"', query)
        
        # Remove quoted phrases from query and split remaining terms
        remaining_query = re.sub(r'"[^"]*"', '', query)
        individual_terms = remaining_query.split()
        
        # Combine all search terms
        search_terms = quoted_phrases + individual_terms
        
        # Remove empty terms
        search_terms = [term.strip() for term in search_terms if term.strip()]
        
        return search_terms
    
    def _document_matches(self, text: str, search_terms: List[str], 
                         case_sensitive: bool = False) -> bool:
        """Check if document text matches all search terms."""
        if not search_terms:
            return False
        
        if not case_sensitive:
            text = text.lower()
            search_terms = [term.lower() for term in search_terms]
        
        # All terms must be found in the text
        for term in search_terms:
            if term not in text:
                return False
        
        return True
    
    def _highlight_matches(self, content: str, search_terms: List[str], 
                          case_sensitive: bool = False) -> str:
        """Highlight search terms in content."""
        if not search_terms:
            return self._truncate_content(content)
        
        highlighted_content = content
        
        # Create regex pattern for highlighting
        for term in search_terms:
            if not term.strip():
                continue
            
            # Escape special regex characters
            escaped_term = re.escape(term)
            
            # Create pattern with word boundaries for better matching
            pattern = r'\b' + escaped_term + r'\b'
            flags = re.IGNORECASE if not case_sensitive else 0
            
            # Replace matches with highlighted version
            highlighted_content = re.sub(
                pattern,
                lambda m: f'<mark style="background-color: yellow; padding: 2px;">{m.group()}</mark>',
                highlighted_content,
                flags=flags
            )
        
        return self._truncate_content(highlighted_content, max_length=2000)
    
    def _truncate_content(self, content: str, max_length: int = 1500) -> str:
        """Truncate content to reasonable length for display."""
        if len(content) <= max_length:
            return content
        
        # Try to find a good breaking point near the max length
        break_point = max_length
        
        # Look for sentence ending near the break point
        for i in range(max_length - 100, max_length + 100):
            if i < len(content) and content[i] in '.!?':
                break_point = i + 1
                break
        
        truncated = content[:break_point].strip()
        
        # Add ellipsis if content was truncated
        if break_point < len(content):
            truncated += "..."
        
        return truncated
    
    def advanced_search(self, documents: List[tuple], 
                       include_terms: List[str] = None,
                       exclude_terms: List[str] = None,
                       category: str = None,
                       file_type: str = None) -> List[Tuple]:
        """
        Perform advanced search with multiple criteria.
        
        Args:
            documents: List of document tuples
            include_terms: Terms that must be present
            exclude_terms: Terms that must not be present
            category: Document category filter
            file_type: File type filter
        """
        results = []
        
        for doc in documents:
            doc_id = doc[0]
            title = doc[2]
            content = doc[3]
            doc_category = doc[6]
            doc_file_type = doc[5]
            
            search_text = f"{title} {content}".lower()
            
            # Apply filters
            if category and doc_category != category:
                continue
            
            if file_type and file_type not in doc_file_type:
                continue
            
            # Check include terms (all must be present)
            if include_terms:
                if not all(term.lower() in search_text for term in include_terms):
                    continue
            
            # Check exclude terms (none should be present)
            if exclude_terms:
                if any(term.lower() in search_text for term in exclude_terms):
                    continue
            
            # Generate highlighted content
            highlight_terms = include_terms or []
            highlighted_content = self._highlight_matches(
                content, highlight_terms, case_sensitive=False
            )
            
            results.append((doc_id, doc, highlighted_content))
        
        return results
    
    def search_by_similarity(self, documents: List[tuple], 
                           reference_content: str, threshold: float = 0.3) -> List[Tuple]:
        """
        Find documents similar to reference content using basic similarity.
        """
        if not reference_content.strip():
            return []
        
        reference_words = set(re.findall(r'\b\w+\b', reference_content.lower()))
        results = []
        
        for doc in documents:
            doc_id = doc[0]
            content = doc[3]
            
            # Calculate basic word overlap similarity
            doc_words = set(re.findall(r'\b\w+\b', content.lower()))
            
            if not doc_words:
                continue
            
            # Jaccard similarity
            intersection = reference_words.intersection(doc_words)
            union = reference_words.union(doc_words)
            
            similarity = len(intersection) / len(union) if union else 0
            
            if similarity >= threshold:
                # Highlight common terms
                common_terms = list(intersection)[:10]  # Limit to 10 terms
                highlighted_content = self._highlight_matches(
                    content, common_terms, case_sensitive=False
                )
                
                results.append((doc_id, doc, highlighted_content))
        
        # Sort by similarity (approximate)
        return results
    
    def get_search_suggestions(self, documents: List[tuple], 
                             partial_query: str, max_suggestions: int = 5) -> List[str]:
        """Generate search suggestions based on document content."""
        if len(partial_query) < 2:
            return []
        
        partial_lower = partial_query.lower()
        suggestions = set()
        
        # Extract words from all documents
        all_words = set()
        for doc in documents:
            content = doc[3].lower()
            words = re.findall(r'\b\w+\b', content)
            all_words.update(words)
        
        # Find words that start with the partial query
        for word in all_words:
            if word.startswith(partial_lower) and len(word) > len(partial_query):
                suggestions.add(word)
                if len(suggestions) >= max_suggestions:
                    break
        
        return sorted(list(suggestions))[:max_suggestions]
