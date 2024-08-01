from dataclasses import dataclass
from pathlib import Path


@dataclass
class Example:
    name: str
    dirpath: Path
    notebook_filepath: Path
