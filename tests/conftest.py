"""Pytest configuration and fixtures."""

from pathlib import Path

import pytest
from ruamel.yaml import YAML

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def v440_full_config():
  """Load full v4.4.0 test config."""
  yaml = YAML()
  with open(FIXTURES_DIR / "v440_full.yaml") as f:
    return yaml.load(f)


@pytest.fixture
def tc3_expected_config():
  """Load expected TC3 output config."""
  yaml = YAML()
  with open(FIXTURES_DIR / "tc3_expected.yaml") as f:
    return yaml.load(f)
