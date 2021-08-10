import pytest
from pathlib import Path

TEST_ROOT = Path(__file__).parent

@pytest.fixture(scope="session")
def files_path():
    return TEST_ROOT / "tests" / "files"
