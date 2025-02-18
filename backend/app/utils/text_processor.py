import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Optional
import re

class TextProcessor:
    def __init__(self):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer()
        
        # Common programming languages and technologies
        self.common_skills = {
            'python', 'java', 'javascript', 'c++', 'ruby', 'php', 'sql',
            'react', 'angular', 'vue', 'node', 'django', 'flask',
            'docker', 'kubernetes', 'aws', 'azure', 'git',
            'machine learning', 'data science', 'artificial intelligence',
            'developer', 'programming'  # Additional common terms
        }
        # Normalize all skills to lowercase
        self.common_skills = {skill.lower() for skill in self.common_skills}

    def preprocess_text(self, text: str) -> str:
        """Clean and tokenize text"""
        # Convert to lowercase
        text = text.lower()
        # Replace special characters with spaces
        text = re.sub(r'[^\w\s]', ' ', text)
        # Tokenize
        tokens = text.split()
        # Remove stopwords and non-alphabetic tokens
        tokens = [token for token in tokens if token.isalpha() and token not in self.stop_words]
        return " ".join(tokens)

    def extract_skills(self, text: str) -> List[str]:
        """Extract potential skills from text using keyword matching"""
        text = text.lower()
        found_skills = set()
        
        # Look for single word skills
        words = set(word_tokenize(text))
        found_skills.update(words.intersection(self.common_skills))
        
        # Look for multi-word skills
        for skill in self.common_skills:
            if ' ' in skill and skill in text:
                found_skills.add(skill)
        
        return list(found_skills)

    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate TF-IDF cosine similarity between two texts"""
        processed_texts = [self.preprocess_text(text1), self.preprocess_text(text2)]
        tfidf_matrix = self.vectorizer.fit_transform(processed_texts)
        return (tfidf_matrix[0] * tfidf_matrix[1].T).toarray()[0, 0]
