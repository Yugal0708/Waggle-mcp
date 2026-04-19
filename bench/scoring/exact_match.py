import re
import string

def normalize_answer(s: str) -> str:
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))

def exact_match_score(prediction: str, ground_truth: str) -> float:
    """Computes exact match score using standard squad normalizations."""
    return 1.0 if normalize_answer(prediction) == normalize_answer(ground_truth) else 0.0

def fuzzy_match_score(prediction: str, ground_truth: str) -> float:
    """A diagnostic containment score, not a publishable benchmark metric."""
    normalized_pred = normalize_answer(prediction)
    normalized_ground_truth = normalize_answer(ground_truth)
    return 1.0 if normalized_ground_truth in normalized_pred else 0.0
