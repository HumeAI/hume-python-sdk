import importlib
import types

import pytest


MODULES_TO_CHECK = [
    "hume",
    "hume.tts",
    "hume.empathic_voice",
    "hume.expression_measurement",
    "hume.expression_measurement.stream",
]


@pytest.mark.parametrize("module_name", MODULES_TO_CHECK)
def test_lazy_submodule_resolution_does_not_recurse(module_name: str) -> None:
    """Modules that lazily expose submodules via _dynamic_imports should not recurse."""
    module = importlib.import_module(module_name)
    dynamic_imports = getattr(module, "_dynamic_imports", {})

    for attr, destination in dynamic_imports.items():
        if destination != ".":
            continue

        submodule = getattr(module, attr)
        assert isinstance(submodule, types.ModuleType)
        assert submodule.__name__.endswith(f"{attr}")
