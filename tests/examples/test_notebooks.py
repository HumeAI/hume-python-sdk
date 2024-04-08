import logging

import pytest
from pytest import TempPathFactory
from testbook import testbook

from tests.examples.example import Example

logger = logging.getLogger(__name__)


@pytest.mark.notebook
@pytest.mark.service
class TestNotebooks:

    @pytest.mark.skip("Notebook environment not activated")
    def test_example_notebook(
        self,
        example: Example,
        tmp_path_factory: TempPathFactory,
        hume_api_key: str,
    ) -> None:
        notebook_text = example.notebook_filepath.read_text()

        # Inject API key for testing
        notebook_text = notebook_text.replace("<your-api-key>", hume_api_key)

        # Inject utilities relative import code
        utilities_import_code = f'import sys; sys.path.append(\\"{example.dirpath}\\"); from utilities'
        notebook_text = notebook_text.replace("from utilities", utilities_import_code)

        # Write temporary notebook file
        temp_notebook_filepath = tmp_path_factory.mktemp("data-dir") / "temp-notebook.ipynb"
        temp_notebook_filepath.write_text(notebook_text)
        logger.info("Temporary notebook written to %s", temp_notebook_filepath)

        with testbook(temp_notebook_filepath, execute=True, kernel_name="hume"):
            pass

    def test_notebook_replaced_api_key(self, example: Example) -> None:
        notebook_text = example.notebook_filepath.read_text()
        if "Client(" in notebook_text:
            assert "<your-api-key>" in notebook_text, "Replace API key!"

    @pytest.mark.skip("Notebook environment not activated")
    def test_notebook_empty_outputs(self, example: Example) -> None:
        with testbook(example.notebook_filepath, execute=False, kernel_name="hume") as notebook:
            for cell in notebook.cells:
                if "outputs" in cell:
                    assert len(cell["outputs"]) == 0, "All notebook cell outputs should be empty"
