"""Pytest configuration and fixtures."""

import sys
from pathlib import Path

import pytest

# Add src directory to Python path for imports
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture(autouse=True)
def reset_settings_cache():
    """Reset settings cache between tests."""
    from e3_e4.config import get_settings
    
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def test_settings():
    """Provide test settings instance."""
    from e3_e4.config import get_test_settings
    
    return get_test_settings(
        environment="testing",
        debug=True,
        log_level="DEBUG",
    )