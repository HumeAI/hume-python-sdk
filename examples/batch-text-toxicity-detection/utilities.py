from __future__ import annotations

from typing import Any


def print_emotions(emotions: list[dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Joy", "Sadness", "Anger"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")


def print_toxicity(toxicity: list[dict[str, Any]]) -> None:
    toxicity_map = {e["name"]: e["score"] for e in toxicity}
    for label in ["toxic", "severe_toxic", "obscene", "threat", "insult", "identity_hate"]:
        print(f"- {label}: {toxicity_map[label]:4f}")
