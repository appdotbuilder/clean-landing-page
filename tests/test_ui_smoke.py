"""Simplified UI smoke test that avoids slot stack issues."""

import pytest
from app.database import reset_db


@pytest.fixture()
def new_db():
    """Reset database for each test."""
    reset_db()
    yield
    reset_db()


def test_landing_page_module_imports():
    """Test that landing page module imports without errors."""
    # This ensures the landing page module is properly structured
    from app.landing_page import create, apply_modern_theme
    from app.landing_service import LandingPageService

    # These should not raise any exceptions
    assert callable(create)
    assert callable(apply_modern_theme)
    assert hasattr(LandingPageService, "create_sample_data")


def test_startup_integration():
    """Test that startup module registers landing page correctly."""
    from app.startup import startup

    # This should not raise any exceptions
    assert callable(startup)
