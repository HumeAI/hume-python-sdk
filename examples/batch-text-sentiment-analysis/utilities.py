from typing import Any, Dict, List


def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Joy", "Sadness", "Anger"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")


def print_sentiment(sentiment: List[Dict[str, Any]]) -> None:
    sentiment_map = {e["name"]: e["score"] for e in sentiment}
    for rating in range(1, 10):
        print(f"- Sentiment {rating}: {sentiment_map[str(rating)]:4f}")
