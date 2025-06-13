from typing import List, Dict, Tuple
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta

class Analytics:
    def __init__(self):
        """Initialize the analytics engine."""
        pass
    
    def generate_statistics(self, documents: List[tuple]) -> Dict:
        """Generate comprehensive statistics from documents."""
        if not documents:
            return {
                'total_documents': 0,
                'total_size': 0,
                'avg_processing_time': 0,
                'categories': {},
                'file_types': {},
                'upload_trends': {},
                'content_stats': {},
                'performance_metrics': {}
            }
        
        stats = {
            'total_documents': len(documents),
            'total_size': sum(doc[4] for doc in documents),
            'avg_processing_time': 0,
            'categories': {},
            'file_types': {},
            'upload_trends': {},
            'content_stats': {},
            'performance_metrics': {}
        }
        
        # Calculate processing time statistics
        processing_times = [doc[8] for doc in documents if doc[8] is not None]
        if processing_times:
            stats['avg_processing_time'] = sum(processing_times) / len(processing_times)
            stats['min_processing_time'] = min(processing_times)
            stats['max_processing_time'] = max(processing_times)
            stats['total_processing_time'] = sum(processing_times)
        
        # Category distribution
        categories = [doc[6] for doc in documents if doc[6]]
        stats['categories'] = dict(Counter(categories))
        
        # File type distribution
        file_types = [doc[5] for doc in documents if doc[5]]
        stats['file_types'] = dict(Counter(file_types))
        
        # Upload trends (by date)
        stats['upload_trends'] = self._calculate_upload_trends(documents)
        
        # Content statistics
        stats['content_stats'] = self._calculate_content_stats(documents)
        
        # Performance metrics
        stats['performance_metrics'] = self._calculate_performance_metrics(documents)
        
        return stats
    
    def _calculate_upload_trends(self, documents: List[tuple]) -> Dict:
        """Calculate upload trends over time."""
        upload_dates = []
        
        for doc in documents:
            upload_date_str = doc[7]  # upload_date
            try:
                # Parse different possible date formats
                if 'T' in upload_date_str:
                    upload_date = datetime.fromisoformat(upload_date_str.replace('Z', ''))
                else:
                    upload_date = datetime.strptime(upload_date_str, '%Y-%m-%d %H:%M:%S')
                upload_dates.append(upload_date)
            except (ValueError, AttributeError):
                continue
        
        if not upload_dates:
            return {}
        
        # Group by day
        daily_counts = defaultdict(int)
        for date in upload_dates:
            day_key = date.strftime('%Y-%m-%d')
            daily_counts[day_key] += 1
        
        # Group by month
        monthly_counts = defaultdict(int)
        for date in upload_dates:
            month_key = date.strftime('%Y-%m')
            monthly_counts[month_key] += 1
        
        return {
            'daily': dict(daily_counts),
            'monthly': dict(monthly_counts),
            'total_days': len(daily_counts),
            'avg_per_day': len(upload_dates) / max(len(daily_counts), 1)
        }
    
    def _calculate_content_stats(self, documents: List[tuple]) -> Dict:
        """Calculate content-related statistics."""
        if not documents:
            return {}
        
        content_lengths = []
        word_counts = []
        title_lengths = []
        
        # Collect all content for analysis
        all_content = ""
        
        for doc in documents:
            content = doc[3]  # content
            title = doc[2]   # title
            
            content_lengths.append(len(content))
            title_lengths.append(len(title))
            
            # Count words
            words = re.findall(r'\b\w+\b', content.lower())
            word_counts.append(len(words))
            
            all_content += " " + content
        
        # Calculate statistics
        stats = {
            'avg_content_length': sum(content_lengths) / len(content_lengths),
            'min_content_length': min(content_lengths),
            'max_content_length': max(content_lengths),
            'avg_word_count': sum(word_counts) / len(word_counts),
            'min_word_count': min(word_counts),
            'max_word_count': max(word_counts),
            'avg_title_length': sum(title_lengths) / len(title_lengths),
            'total_words': sum(word_counts),
            'unique_words': len(set(re.findall(r'\b\w+\b', all_content.lower()))),
        }
        
        # Most common words
        all_words = re.findall(r'\b\w+\b', all_content.lower())
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'this', 'that', 'these', 'those', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'it', 'its', 'he', 'she', 'they', 'we', 'you', 'i', 'me', 'him', 'her', 'them', 'us'}
        filtered_words = [word for word in all_words if word not in stop_words and len(word) > 2]
        
        word_freq = Counter(filtered_words)
        stats['most_common_words'] = dict(word_freq.most_common(10))
        
        return stats
    
    def _calculate_performance_metrics(self, documents: List[tuple]) -> Dict:
        """Calculate performance-related metrics."""
        if not documents:
            return {}
        
        # Group by file size ranges
        size_ranges = {
            'small': 0,    # < 1MB
            'medium': 0,   # 1MB - 10MB
            'large': 0,    # 10MB - 100MB
            'xlarge': 0    # > 100MB
        }
        
        processing_by_size = defaultdict(list)
        
        for doc in documents:
            file_size = doc[4]  # file_size
            processing_time = doc[8]  # processing_time
            
            # Categorize by size
            if file_size < 1024 * 1024:  # < 1MB
                size_ranges['small'] += 1
                if processing_time:
                    processing_by_size['small'].append(processing_time)
            elif file_size < 10 * 1024 * 1024:  # < 10MB
                size_ranges['medium'] += 1
                if processing_time:
                    processing_by_size['medium'].append(processing_time)
            elif file_size < 100 * 1024 * 1024:  # < 100MB
                size_ranges['large'] += 1
                if processing_time:
                    processing_by_size['large'].append(processing_time)
            else:  # >= 100MB
                size_ranges['xlarge'] += 1
                if processing_time:
                    processing_by_size['xlarge'].append(processing_time)
        
        # Calculate average processing time by size
        avg_processing_by_size = {}
        for size_cat, times in processing_by_size.items():
            if times:
                avg_processing_by_size[size_cat] = sum(times) / len(times)
        
        return {
            'size_distribution': size_ranges,
            'avg_processing_by_size': avg_processing_by_size,
            'processing_efficiency': self._calculate_efficiency_score(documents)
        }
    
    def _calculate_efficiency_score(self, documents: List[tuple]) -> float:
        """Calculate an efficiency score based on processing time vs file size."""
        if not documents:
            return 0.0
        
        efficiency_scores = []
        
        for doc in documents:
            file_size = doc[4]  # file_size in bytes
            processing_time = doc[8]  # processing_time in seconds
            
            if processing_time and processing_time > 0 and file_size > 0:
                # Calculate MB per second
                mb_size = file_size / (1024 * 1024)
                mb_per_second = mb_size / processing_time
                efficiency_scores.append(mb_per_second)
        
        if efficiency_scores:
            return sum(efficiency_scores) / len(efficiency_scores)
        
        return 0.0
    
    def get_category_analysis(self, documents: List[tuple]) -> Dict:
        """Get detailed analysis for each category."""
        category_analysis = defaultdict(lambda: {
            'count': 0,
            'total_size': 0,
            'avg_size': 0,
            'total_processing_time': 0,
            'avg_processing_time': 0,
            'file_types': defaultdict(int)
        })
        
        for doc in documents:
            category = doc[6] or 'Uncategorized'
            file_size = doc[4]
            processing_time = doc[8] or 0
            file_type = doc[5]
            
            category_analysis[category]['count'] += 1
            category_analysis[category]['total_size'] += file_size
            category_analysis[category]['total_processing_time'] += processing_time
            category_analysis[category]['file_types'][file_type] += 1
        
        # Calculate averages
        for category in category_analysis:
            count = category_analysis[category]['count']
            if count > 0:
                category_analysis[category]['avg_size'] = (
                    category_analysis[category]['total_size'] / count
                )
                category_analysis[category]['avg_processing_time'] = (
                    category_analysis[category]['total_processing_time'] / count
                )
                # Convert defaultdict to regular dict for JSON serialization
                category_analysis[category]['file_types'] = dict(
                    category_analysis[category]['file_types']
                )
        
        return dict(category_analysis)
    
    def get_search_analytics(self, search_history: List[Dict]) -> Dict:
        """Analyze search patterns (if search history is available)."""
        if not search_history:
            return {}
        
        search_terms = []
        search_times = []
        
        for search in search_history:
            search_terms.extend(search.get('terms', []))
            search_times.append(search.get('timestamp'))
        
        # Most common search terms
        term_frequency = Counter(search_terms)
        
        return {
            'total_searches': len(search_history),
            'unique_terms': len(set(search_terms)),
            'most_searched_terms': dict(term_frequency.most_common(10)),
            'search_frequency': len(search_history) / max(len(set(search_times)), 1)
        }
    
    def export_analytics_report(self, documents: List[tuple]) -> str:
        """Export a comprehensive analytics report as text."""
        stats = self.generate_statistics(documents)
        
        report = "DOCUMENT ANALYTICS REPORT\n"
        report += "=" * 50 + "\n\n"
        
        # Basic Statistics
        report += "BASIC STATISTICS\n"
        report += "-" * 20 + "\n"
        report += f"Total Documents: {stats['total_documents']}\n"
        report += f"Total Size: {stats['total_size'] / (1024*1024):.2f} MB\n"
        report += f"Average Processing Time: {stats['avg_processing_time']:.2f} seconds\n\n"
        
        # Categories
        if stats['categories']:
            report += "DOCUMENT CATEGORIES\n"
            report += "-" * 20 + "\n"
            for category, count in stats['categories'].items():
                percentage = (count / stats['total_documents']) * 100
                report += f"{category}: {count} ({percentage:.1f}%)\n"
            report += "\n"
        
        # File Types
        if stats['file_types']:
            report += "FILE TYPES\n"
            report += "-" * 20 + "\n"
            for file_type, count in stats['file_types'].items():
                percentage = (count / stats['total_documents']) * 100
                report += f"{file_type}: {count} ({percentage:.1f}%)\n"
            report += "\n"
        
        # Content Statistics
        if stats['content_stats']:
            content_stats = stats['content_stats']
            report += "CONTENT ANALYSIS\n"
            report += "-" * 20 + "\n"
            report += f"Average Content Length: {content_stats.get('avg_content_length', 0):.0f} characters\n"
            report += f"Average Word Count: {content_stats.get('avg_word_count', 0):.0f} words\n"
            report += f"Total Unique Words: {content_stats.get('unique_words', 0)}\n"
            
            if 'most_common_words' in content_stats:
                report += "\nMost Common Words:\n"
                for word, count in list(content_stats['most_common_words'].items())[:5]:
                    report += f"  {word}: {count}\n"
            report += "\n"
        
        # Performance Metrics
        if stats['performance_metrics']:
            perf = stats['performance_metrics']
            report += "PERFORMANCE METRICS\n"
            report += "-" * 20 + "\n"
            
            if 'size_distribution' in perf:
                report += "Size Distribution:\n"
                for size_cat, count in perf['size_distribution'].items():
                    report += f"  {size_cat}: {count}\n"
            
            if 'processing_efficiency' in perf:
                report += f"Processing Efficiency: {perf['processing_efficiency']:.2f} MB/second\n"
        
        report += "\nReport generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        return report
