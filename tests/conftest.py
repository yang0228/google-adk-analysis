import importlib.util
import sys
import uuid
from pathlib import Path

import pytest


@pytest.fixture
def load_example():
    loaded = []

    def load(name):
        path = Path(__file__).resolve().parents[1] / "examples" / name / "main.py"
        module_name = "example_" + uuid.uuid4().hex
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        loaded.append(module_name)
        spec.loader.exec_module(module)
        return module

    yield load
    for name in loaded:
        sys.modules.pop(name, None)
