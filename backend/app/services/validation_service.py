from typing import List, Dict, Tuple
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class ValidationService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.match_scores: List[float] = []
        self.user_feedback: List[Dict] = []

    def validate_skill_extraction(self, predicted_skills: List[str], actual_skills: List[str]) -> Dict[str, float]:
        """Calculate precision, recall, and F1 score for skill extraction"""
        # Convert skills to binary vectors
        all_skills = list(set(predicted_skills + actual_skills))
        y_true = [1 if skill in actual_skills else 0 for skill in all_skills]
        y_pred = [1 if skill in predicted_skills else 0 for skill in all_skills]
        
        # Calculate metrics
        precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='binary')
        accuracy = accuracy_score(y_true, y_pred)
        
        return {
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "accuracy": accuracy
        }

    def calculate_match_similarity(self, text1: str, text2: str) -> float:
        """Calculate TF-IDF similarity between two texts"""
        tfidf_matrix = self.vectorizer.fit_transform([text1, text2])
        return (tfidf_matrix * tfidf_matrix.T).toarray()[0, 1]

    def record_match_score(self, score: float) -> None:
        """Record a match score for distribution analysis"""
        self.match_scores.append(score)

    def get_score_distribution(self) -> Dict[str, float]:
        """Calculate statistics for match score distribution"""
        if not self.match_scores:
            return {"mean": 0, "std": 0, "median": 0}
            
        scores = np.array(self.match_scores)
        return {
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "median": float(np.median(scores))
        }

    def record_user_feedback(self, match_id: str, feedback: Dict) -> None:
        """Record user feedback for a match"""
        self.user_feedback.append({
            "match_id": match_id,
            "feedback": feedback,
            "timestamp": np.datetime64('now')
        })

    def get_feedback_summary(self) -> Dict[str, float]:
        """Calculate summary statistics from user feedback"""
        if not self.user_feedback:
            return {"average_rating": 0, "feedback_count": 0}
            
        ratings = [f["feedback"].get("rating", 0) for f in self.user_feedback]
        return {
            "average_rating": float(np.mean(ratings)),
            "feedback_count": len(ratings)
        }
