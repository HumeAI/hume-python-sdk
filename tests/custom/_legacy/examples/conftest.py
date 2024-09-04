import re
from pathlib import Path
from typing import Generator

import pytest
from pytest import FixtureRequest

from tests.custom._legacy.examples.example import Example


def get_example_dirpaths() -> list[Path]:
    examples_dirpath = Path(__file__).parent.parent.parent.parent.parent / "examples"
    paths = []
    for example_dirpath in examples_dirpath.iterdir():
        if example_dirpath.is_dir():
            paths.append(example_dirpath)
    assert len(paths) > 5
    return paths


def get_examples() -> list[Example]:
    examples = []
    for dirpath in get_example_dirpaths():
        dirname = dirpath.name
        assert dirname.split("-")[0] in ["stream", "batch", "evi"]
        assert re.match("^[a-z-]+$", dirname) is not None
        notebook_name = dirname.replace("_", "-")
        notebook_filepath = dirpath / f"{notebook_name}.ipynb"
        assert notebook_filepath.is_file()
        example = Example(
            name=notebook_name,
            dirpath=dirpath,
            notebook_filepath=notebook_filepath,
        )
        examples.append(example)
    return examples


@pytest.fixture(scope="session")
def examples() -> list[Example]:
    return get_examples()


def get_example_id(example: Example) -> str:
    return example.name


@pytest.fixture(scope="session", params=get_examples(), ids=get_example_id)
def example(request: FixtureRequest) -> Generator[Example, None, None]:
    yield request.param
