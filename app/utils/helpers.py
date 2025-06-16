import re
from typing import List, Dict
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class TextProcessor:
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s.,!?-]', '', text)
        return text.strip()
    
    @staticmethod
    def extract_keywords(text: str, top_n: int = 10) -> List[str]:
        """Extract important keywords from text"""
        try:
            # Tokenize and remove stopwords
            words = word_tokenize(text.lower())
            stop_words = set(stopwords.words('english'))
            
            # Filter words
            keywords = [
                word for word in words 
                if word.isalpha() and len(word) > 3 and word not in stop_words
            ]
            
            # Count frequency
            word_freq = {}
            for word in keywords:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Return top keywords
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
            return [word for word, freq in sorted_words[:top_n]]
            
        except Exception as e:
            print(f"Error extracting keywords: {e}")
            return []
    
    @staticmethod
    def calculate_text_metrics(text: str) -> Dict[str, float]:
        """Calculate various text quality metrics"""
        words = len(text.split())
        sentences = len(re.findall(r'[.!?]+', text))
        characters = len(text)
        
        avg_word_length = sum(len(word) for word in text.split()) / words if words > 0 else 0
        avg_sentence_length = words / sentences if sentences > 0 else 0
        
        return {
            "word_count": words,
            "sentence_count": sentences,
            "character_count": characters,
            "avg_word_length": avg_word_length,
            "avg_sentence_length": avg_sentence_length
        }

class BiasKeywords:
    """Comprehensive bias keyword lists for various categories"""
    
    GENDER_MASCULINE = [
        'aggressive', 'ambitious', 'assertive', 'competitive', 'confident', 
        'decisive', 'determined', 'dominant', 'independent', 'leader',
        'outspoken', 'self-reliant', 'strong', 'superior', 'active',
        'adventurous', 'analytical', 'defend', 'challenge', 'individual'
    ]
    
    GENDER_FEMININE = [
        'collaborative', 'cooperative', 'dependable', 'honest', 
        'interpersonal', 'loyal', 'pleasant', 'polite', 'quiet',
        'responsible', 'supportive', 'sympathetic', 'team player', 
        'trustworthy', 'understanding', 'yielding', 'gentle', 'caring'
    ]
    
    AGE_BIAS = [
        'young', 'energetic', 'recent graduate', 'fresh', 'new grad',
        'digital native', 'up-and-coming', 'mature', 'experienced',
        'seasoned', 'senior', 'veteran', 'established', 'junior'
    ]
    
    CULTURAL_BIAS = [
        'native english speaker', 'american-born', 'cultural fit',
        'traditional values', 'mainstream', 'conventional', 'normal',
        'standard background', 'typical', 'regular'
    ]
    
    EXCLUSIONARY_TERMS = [
        'guys', 'brotherhood', 'fraternity', 'manpower', 'chairman',
        'salesman', 'spokesman', 'workman', 'businessman', 'craftsman'
    ]
    
    INCLUSIVE_ALTERNATIVES = {
        'guys': 'everyone/team/folks',
        'brotherhood': 'community/fellowship',
        'chairman': 'chairperson/chair',
        'salesman': 'salesperson/sales representative',
        'spokesman': 'spokesperson/representative',
        'manpower': 'workforce/personnel/staff'
    }
