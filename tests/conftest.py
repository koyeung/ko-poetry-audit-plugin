from pathlib import Path

import pytest


@pytest.fixture
def test_data():
    return Path(__file__).with_name("data")
