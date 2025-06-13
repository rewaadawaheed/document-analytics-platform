import re
from typing import List, Dict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import os

class DocumentClassifier:
    def __init__(self):
        """Initialize the document classifier."""
        self.categories = [
            'Business', 'Technical', 'Legal', 'Medical', 'Academic', 
            'Financial', 'Marketing', 'Research', 'Report', 'Scientific',
            'Educational', 'Government', 'News', 'Entertainment', 'Sports',
            'Travel', 'Food', 'Technology', 'Healthcare', 'Real Estate',
            'Insurance', 'Banking', 'Construction', 'Manufacturing', 'Retail',
            'Transportation', 'Energy', 'Environmental', 'Social Media',
            'Web Content', 'Blog', 'Tutorial', 'Manual', 'Policy', 'Other'
        ]
        
        # Keywords for each category
        self.category_keywords = {
            'Business': [
                'business', 'company', 'corporation', 'enterprise', 'organization',
                'management', 'strategy', 'marketing', 'sales', 'revenue', 'profit',
                'customer', 'client', 'market', 'industry', 'competition', 'planning',
                'proposal', 'contract', 'agreement', 'partnership', 'merger', 'acquisition'
            ],
            'Technical': [
                'technical', 'technology', 'software', 'hardware', 'system', 'computer',
                'programming', 'code', 'development', 'engineering', 'algorithm',
                'database', 'network', 'security', 'infrastructure', 'architecture',
                'specification', 'documentation', 'manual', 'api', 'framework', 'protocol'
            ],
            'Legal': [
                'legal', 'law', 'court', 'judge', 'lawyer', 'attorney', 'litigation',
                'contract', 'agreement', 'terms', 'conditions', 'clause', 'regulation',
                'compliance', 'statute', 'legislation', 'judicial', 'plaintiff', 'defendant',
                'evidence', 'testimony', 'verdict', 'settlement', 'damages', 'liability'
            ],
            'Medical': [
                'medical', 'health', 'healthcare', 'hospital', 'patient', 'doctor',
                'physician', 'nurse', 'treatment', 'diagnosis', 'therapy', 'medication',
                'drug', 'disease', 'symptom', 'clinical', 'pharmaceutical', 'surgery',
                'anatomy', 'physiology', 'pathology', 'radiology', 'laboratory', 'vaccine'
            ],
            'Academic': [
                'academic', 'research', 'study', 'university', 'college', 'education',
                'student', 'professor', 'faculty', 'curriculum', 'course', 'degree',
                'thesis', 'dissertation', 'journal', 'publication', 'conference',
                'methodology', 'analysis', 'experiment', 'hypothesis', 'theory', 'literature'
            ],
            'Financial': [
                'financial', 'finance', 'money', 'investment', 'banking', 'credit',
                'loan', 'debt', 'budget', 'accounting', 'audit', 'tax', 'income',
                'expense', 'asset', 'liability', 'equity', 'portfolio', 'stock',
                'bond', 'securities', 'insurance', 'pension', 'fund', 'capital'
            ],
            'Marketing': [
                'marketing', 'advertising', 'promotion', 'campaign', 'brand', 'branding',
                'customer', 'consumer', 'target', 'audience', 'demographic', 'segment',
                'product', 'service', 'pricing', 'distribution', 'channel', 'retail',
                'digital', 'social', 'media', 'content', 'seo', 'analytics', 'conversion'
            ],
            'Research': [
                'research', 'study', 'analysis', 'investigation', 'survey', 'experiment',
                'data', 'results', 'findings', 'conclusion', 'methodology', 'sample',
                'hypothesis', 'statistical', 'quantitative', 'qualitative', 'empirical',
                'observation', 'measurement', 'correlation', 'regression', 'significance'
            ],
            'Report': [
                'report', 'summary', 'overview', 'executive', 'quarterly', 'annual',
                'progress', 'status', 'update', 'performance', 'metrics', 'kpi',
                'dashboard', 'benchmark', 'evaluation', 'assessment', 'review',
                'recommendation', 'conclusion', 'action', 'plan', 'forecast', 'projection'
            ],
            'Scientific': [
                'research', 'experiment', 'hypothesis', 'methodology', 'data', 'analysis',
                'results', 'conclusion', 'peer', 'review', 'publication', 'journal',
                'laboratory', 'study', 'observation', 'measurement', 'theory', 'model',
                'validation', 'statistical', 'significance', 'correlation', 'causation'
            ],
            'Educational': [
                'education', 'learning', 'teaching', 'curriculum', 'lesson', 'course',
                'training', 'workshop', 'seminar', 'tutorial', 'instruction', 'guide',
                'knowledge', 'skill', 'competency', 'assessment', 'evaluation', 'grade',
                'student', 'teacher', 'instructor', 'professor', 'classroom', 'online'
            ],
            'Government': [
                'government', 'policy', 'regulation', 'legislation', 'law', 'statute',
                'ordinance', 'rule', 'compliance', 'enforcement', 'agency', 'department',
                'ministry', 'bureau', 'commission', 'authority', 'public', 'service',
                'administration', 'official', 'federal', 'state', 'local', 'municipal'
            ],
            'News': [
                'news', 'article', 'breaking', 'headline', 'story', 'reporter', 'journalist',
                'press', 'media', 'coverage', 'interview', 'statement', 'announcement',
                'update', 'bulletin', 'broadcast', 'publication', 'editorial', 'opinion',
                'current', 'events', 'happening', 'developing', 'latest', 'recent'
            ],
            'Entertainment': [
                'entertainment', 'movie', 'film', 'television', 'tv', 'show', 'series',
                'music', 'song', 'album', 'artist', 'performer', 'actor', 'actress',
                'celebrity', 'star', 'fame', 'popular', 'culture', 'gaming', 'game',
                'sport', 'recreation', 'leisure', 'fun', 'enjoyment', 'amusement'
            ],
            'Sports': [
                'sports', 'football', 'basketball', 'baseball', 'soccer', 'tennis',
                'golf', 'hockey', 'volleyball', 'swimming', 'running', 'marathon',
                'athlete', 'player', 'team', 'coach', 'training', 'competition',
                'tournament', 'championship', 'league', 'season', 'game', 'match'
            ],
            'Travel': [
                'travel', 'trip', 'vacation', 'holiday', 'destination', 'tourism',
                'hotel', 'accommodation', 'flight', 'airline', 'airport', 'booking',
                'reservation', 'itinerary', 'guide', 'attraction', 'sightseeing',
                'adventure', 'exploration', 'journey', 'expedition', 'cruise', 'resort'
            ],
            'Food': [
                'food', 'recipe', 'cooking', 'cuisine', 'restaurant', 'menu', 'dish',
                'ingredient', 'nutrition', 'diet', 'healthy', 'organic', 'fresh',
                'meal', 'breakfast', 'lunch', 'dinner', 'snack', 'beverage', 'drink',
                'chef', 'kitchen', 'preparation', 'flavor', 'taste', 'delicious'
            ],
            'Technology': [
                'technology', 'innovation', 'digital', 'computer', 'software', 'hardware',
                'internet', 'web', 'mobile', 'app', 'application', 'platform', 'system',
                'data', 'cloud', 'artificial', 'intelligence', 'machine', 'learning',
                'automation', 'robotics', 'blockchain', 'cryptocurrency', 'cybersecurity'
            ],
            'Healthcare': [
                'healthcare', 'health', 'medical', 'medicine', 'treatment', 'therapy',
                'diagnosis', 'patient', 'doctor', 'nurse', 'hospital', 'clinic',
                'pharmaceutical', 'drug', 'medication', 'disease', 'illness', 'condition',
                'prevention', 'wellness', 'fitness', 'exercise', 'mental', 'physical'
            ],
            'Real Estate': [
                'real', 'estate', 'property', 'house', 'home', 'apartment', 'condo',
                'residential', 'commercial', 'industrial', 'land', 'lot', 'building',
                'construction', 'development', 'investment', 'mortgage', 'loan', 'rent',
                'lease', 'buy', 'sell', 'market', 'value', 'appraisal', 'agent', 'broker'
            ],
            'Insurance': [
                'insurance', 'policy', 'coverage', 'premium', 'claim', 'deductible',
                'liability', 'auto', 'health', 'life', 'property', 'casualty',
                'underwriting', 'risk', 'assessment', 'protection', 'benefit', 'compensation',
                'reimbursement', 'settlement', 'adjuster', 'agent', 'broker', 'carrier'
            ],
            'Banking': [
                'banking', 'bank', 'account', 'savings', 'checking', 'deposit', 'withdrawal',
                'transfer', 'transaction', 'balance', 'interest', 'rate', 'loan', 'credit',
                'mortgage', 'investment', 'portfolio', 'financial', 'money', 'currency',
                'payment', 'card', 'atm', 'branch', 'online', 'mobile'
            ],
            'Construction': [
                'construction', 'building', 'contractor', 'architect', 'engineer', 'project',
                'site', 'material', 'concrete', 'steel', 'wood', 'foundation', 'structure',
                'design', 'blueprint', 'permit', 'safety', 'equipment', 'machinery',
                'worker', 'labor', 'cost', 'budget', 'schedule', 'timeline', 'completion'
            ],
            'Manufacturing': [
                'manufacturing', 'production', 'factory', 'plant', 'assembly', 'line',
                'process', 'quality', 'control', 'inspection', 'testing', 'machinery',
                'equipment', 'automation', 'efficiency', 'output', 'capacity', 'supply',
                'chain', 'inventory', 'raw', 'material', 'finished', 'goods', 'warehouse'
            ],
            'Retail': [
                'retail', 'store', 'shop', 'customer', 'sale', 'purchase', 'product',
                'merchandise', 'inventory', 'stock', 'price', 'discount', 'promotion',
                'marketing', 'advertising', 'brand', 'display', 'checkout', 'payment',
                'service', 'experience', 'satisfaction', 'loyalty', 'return', 'exchange'
            ],
            'Transportation': [
                'transportation', 'transport', 'vehicle', 'car', 'truck', 'bus', 'train',
                'airplane', 'ship', 'freight', 'cargo', 'delivery', 'logistics', 'route',
                'traffic', 'road', 'highway', 'infrastructure', 'fuel', 'maintenance',
                'safety', 'regulation', 'license', 'permit', 'driver', 'passenger'
            ],
            'Energy': [
                'energy', 'power', 'electricity', 'solar', 'wind', 'nuclear', 'coal',
                'oil', 'gas', 'renewable', 'sustainable', 'grid', 'generation', 'consumption',
                'efficiency', 'conservation', 'utility', 'plant', 'facility', 'resource',
                'fuel', 'battery', 'storage', 'transmission', 'distribution', 'cost'
            ],
            'Environmental': [
                'environmental', 'environment', 'ecology', 'climate', 'weather', 'pollution',
                'contamination', 'waste', 'recycling', 'sustainability', 'conservation',
                'protection', 'wildlife', 'habitat', 'ecosystem', 'biodiversity', 'carbon',
                'emission', 'greenhouse', 'global', 'warming', 'renewable', 'clean', 'green'
            ],
            'Social Media': [
                'social', 'media', 'facebook', 'twitter', 'instagram', 'linkedin', 'youtube',
                'post', 'share', 'like', 'comment', 'follow', 'follower', 'friend', 'network',
                'platform', 'content', 'viral', 'trending', 'hashtag', 'influence', 'engagement',
                'community', 'online', 'digital', 'communication', 'interaction', 'connection'
            ],
            'Web Content': [
                'web', 'website', 'page', 'content', 'blog', 'article', 'post', 'online',
                'internet', 'digital', 'html', 'css', 'javascript', 'responsive', 'design',
                'user', 'experience', 'interface', 'navigation', 'link', 'url', 'domain',
                'hosting', 'server', 'database', 'cms', 'wordpress', 'seo', 'optimization'
            ],
            'Blog': [
                'blog', 'blogger', 'blogging', 'post', 'article', 'content', 'writing',
                'author', 'publish', 'share', 'comment', 'reader', 'audience', 'topic',
                'category', 'tag', 'archive', 'feed', 'rss', 'subscribe', 'follow',
                'personal', 'opinion', 'experience', 'story', 'diary', 'journal'
            ],
            'Tutorial': [
                'tutorial', 'guide', 'how', 'to', 'step', 'instruction', 'lesson', 'learn',
                'teach', 'explain', 'demonstrate', 'example', 'practice', 'exercise',
                'walkthrough', 'course', 'training', 'skill', 'technique', 'method',
                'procedure', 'process', 'beginner', 'advanced', 'tips', 'tricks'
            ],
            'Manual': [
                'manual', 'handbook', 'guide', 'instruction', 'documentation', 'reference',
                'specification', 'procedure', 'operation', 'maintenance', 'troubleshooting',
                'installation', 'setup', 'configuration', 'user', 'technical', 'service',
                'repair', 'warranty', 'safety', 'precaution', 'warning', 'caution'
            ],
            'Policy': [
                'policy', 'procedure', 'guideline', 'rule', 'regulation', 'standard',
                'protocol', 'directive', 'instruction', 'requirement', 'compliance',
                'governance', 'framework', 'structure', 'process', 'workflow', 'approval',
                'authorization', 'responsibility', 'accountability', 'enforcement', 'violation'
            ]
        }
        
        self.model = None
        self.is_trained = False
        
        # Try to load pre-trained model
        self._load_model()
    
    def classify_document(self, content: str) -> str:
        """Classify a document based on its content."""
        if not content.strip():
            return 'Other'
        
        # Use keyword-based classification
        return self._classify_by_keywords(content)
    
    def _classify_by_keywords(self, content: str) -> str:
        """Classify document using keyword matching."""
        content_lower = content.lower()
        
        # Remove punctuation and split into words
        words = re.findall(r'\b\w+\b', content_lower)
        word_set = set(words)
        
        # Calculate scores for each category
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                # Count exact matches
                if keyword in word_set:
                    score += 1
                
                # Count partial matches in the full content
                score += content_lower.count(keyword) * 0.5
            
            # Normalize by keyword count
            category_scores[category] = score / len(keywords)
        
        # Find the category with the highest score
        if category_scores:
            best_category = max(category_scores.keys(), key=lambda k: category_scores[k])
            best_score = category_scores[best_category]
            
            # Only return category if score is above threshold
            if best_score > 0.1:  # Adjust threshold as needed
                return best_category
        
        return 'Other'
    
    def train_classifier(self, documents: List[tuple]) -> bool:
        """Train the classifier using existing documents."""
        if len(documents) < 10:  # Need minimum documents for training
            return False
        
        # Prepare training data
        texts = []
        labels = []
        
        for doc in documents:
            if doc[6]:  # If category exists
                texts.append(doc[3])  # content
                labels.append(doc[6])  # category
        
        if len(set(labels)) < 2:  # Need at least 2 different categories
            return False
        
        try:
            # Create and train the model
            self.model = Pipeline([
                ('tfidf', TfidfVectorizer(max_features=1000, stop_words='english')),
                ('classifier', MultinomialNB())
            ])
            
            self.model.fit(texts, labels)
            self.is_trained = True
            
            # Save the trained model
            self._save_model()
            
            return True
            
        except Exception as e:
            print(f"Training failed: {str(e)}")
            return False
    
    def _classify_with_ml(self, content: str) -> str:
        """Classify document using trained ML model."""
        if not self.is_trained or not self.model:
            return self._classify_by_keywords(content)
        
        try:
            prediction = self.model.predict([content])[0]
            return prediction
        except Exception:
            # Fallback to keyword-based classification
            return self._classify_by_keywords(content)
    
    def _save_model(self):
        """Save the trained model to disk."""
        if self.model and self.is_trained:
            try:
                with open('classifier_model.pkl', 'wb') as f:
                    pickle.dump(self.model, f)
            except Exception:
                pass  # Silent fail for model saving
    
    def _load_model(self):
        """Load a pre-trained model from disk."""
        try:
            if os.path.exists('classifier_model.pkl'):
                with open('classifier_model.pkl', 'rb') as f:
                    self.model = pickle.load(f)
                    self.is_trained = True
        except Exception:
            pass  # Silent fail for model loading
    
    def get_categories(self) -> List[str]:
        """Get list of available categories."""
        return self.categories.copy()
    
    def get_category_keywords(self, category: str) -> List[str]:
        """Get keywords for a specific category."""
        return self.category_keywords.get(category, [])
    
    def add_category_keywords(self, category: str, keywords: List[str]):
        """Add keywords to a category."""
        if category in self.category_keywords:
            self.category_keywords[category].extend(keywords)
        else:
            self.category_keywords[category] = keywords
            if category not in self.categories:
                self.categories.append(category)
    
    def classify_batch(self, documents: List[str]) -> List[str]:
        """Classify multiple documents at once."""
        classifications = []
        
        for content in documents:
            classification = self.classify_document(content)
            classifications.append(classification)
        
        return classifications
    
    def get_classification_confidence(self, content: str) -> Dict[str, float]:
        """Get classification confidence scores for all categories."""
        content_lower = content.lower()
        words = re.findall(r'\b\w+\b', content_lower)
        word_set = set(words)
        
        category_scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for keyword in keywords:
                if keyword in word_set:
                    score += 1
                score += content_lower.count(keyword) * 0.5
            
            # Normalize by keyword count
            normalized_score = score / len(keywords) if keywords else 0
            category_scores[category] = min(normalized_score, 1.0)  # Cap at 1.0
        
        return category_scores
