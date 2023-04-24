from pathlib import Path
from typing import Any, Dict, Iterator, List

from urllib.request import urlretrieve

from pydub import AudioSegment


def download_file(url: str) -> Path:
    example_dirpath = Path(__file__).parent
    data_dirpath = example_dirpath / "data"
    data_dirpath.mkdir(exist_ok=True)
    filepath = data_dirpath / Path(url).name

    print("Downloaded media file from: ", url)
    urlretrieve(url, filepath)
    return filepath


def print_emotions(emotions: List[Dict[str, Any]]) -> None:
    emotion_map = {e["name"]: e["score"] for e in emotions}
    for emotion in ["Joy", "Sadness", "Anger"]:
        print(f"- {emotion}: {emotion_map[emotion]:4f}")


def generate_audio_stream(filepath: Path) -> Iterator[AudioSegment]:
    segment = AudioSegment.from_file(filepath)

    chunk_size = 3000
    chunk_count = 0
    while True:
        start_time = chunk_count * chunk_size
        end_time = start_time + chunk_size
        if start_time > len(segment):
            return
        yield segment[start_time:end_time]
        chunk_count += 1
