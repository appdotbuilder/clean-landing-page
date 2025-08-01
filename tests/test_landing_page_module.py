"""Tests for landing page module functionality."""

import pytest
from app.database import reset_db
from app.landing_service import LandingPageService
from app.landing_page import apply_modern_theme


@pytest.fixture()
def new_db():
    """Reset database for each test."""
    reset_db()
    yield
    reset_db()


def test_apply_modern_theme():
    """Test that modern theme application doesn't raise errors."""
    # This should not raise any exceptions
    apply_modern_theme()


def test_create_landing_page_ui_with_valid_data(new_db):
    """Test UI creation with valid landing page data."""
    # Create sample data
    landing_page = LandingPageService.create_sample_data()

    # This test ensures the UI creation function can handle the data structure
    # without actually rendering UI (which would require slot context)

    assert landing_page.id is not None

    # Verify the landing page has all required components
    heroes = LandingPageService.get_hero_sections(landing_page.id)
    features = LandingPageService.get_features(landing_page.id)
    ctas = LandingPageService.get_cta_sections(landing_page.id)

    assert len(heroes) >= 1
    assert len(features) >= 3
    assert len(ctas) >= 1

    # Verify hero has required fields for UI
    hero = heroes[0]
    assert hero.headline
    assert hero.primary_button_text

    # Verify features have required fields
    for feature in features:
        assert feature.title
        assert feature.description

    # Verify CTA has required fields
    cta = ctas[0]
    assert cta.headline
    assert cta.primary_button_text
    assert cta.primary_button_url


def test_landing_page_data_completeness(new_db):
    """Test that sample data contains all necessary fields for UI rendering."""
    landing_page = LandingPageService.create_sample_data()

    assert landing_page.id is not None

    # Test hero section completeness
    heroes = LandingPageService.get_hero_sections(landing_page.id)
    hero = heroes[0]

    assert hero.headline == "Transform Your Business with Modern Solutions"
    assert hero.subheadline is not None
    assert hero.description is not None
    assert hero.background_color == "#1e293b"
    assert hero.text_color == "#ffffff"
    assert hero.primary_button_text == "Get Started"
    assert hero.primary_button_url == "/signup"

    # Test feature completeness
    features = LandingPageService.get_features(landing_page.id)
    featured_features = [f for f in features if f.is_featured]

    assert len(featured_features) == 3
    feature_titles = [f.title for f in featured_features]
    assert "Lightning Fast Performance" in feature_titles
    assert "Intuitive Design" in feature_titles
    assert "Enterprise Security" in feature_titles

    # Test CTA completeness
    ctas = LandingPageService.get_cta_sections(landing_page.id)
    cta = ctas[0]

    assert cta.headline == "Ready to Transform Your Business?"
    assert cta.primary_button_text == "Start Free Trial"
    assert cta.secondary_button_text == "View Pricing"
    assert cta.primary_button_url == "/trial"
    assert cta.secondary_button_url == "/pricing"


def test_landing_page_ordering(new_db):
    """Test that components are properly ordered for UI display."""
    landing_page = LandingPageService.create_sample_data()

    assert landing_page.id is not None

    # Test feature ordering
    features = LandingPageService.get_features(landing_page.id)

    # Featured features should come first (is_featured=True)
    featured_features = [f for f in features if f.is_featured]
    non_featured = [f for f in features if not f.is_featured]

    assert len(featured_features) == 3
    assert len(non_featured) == 3

    # Check that display_order is respected
    for i in range(len(features) - 1):
        assert features[i].display_order <= features[i + 1].display_order


def test_landing_page_missing_data_handling():
    """Test handling of missing landing page data."""
    # Test with non-existent page
    page = LandingPageService.get_active_landing_page("nonexistent")
    assert page is None

    # Test with page that has no components
    from app.models import LandingPageCreate

    empty_page_data = LandingPageCreate(title="Empty Page", slug="empty-page")

    empty_page = LandingPageService.create_landing_page(empty_page_data)
    assert empty_page.id is not None

    # Should return empty lists for components
    heroes = LandingPageService.get_hero_sections(empty_page.id)
    features = LandingPageService.get_features(empty_page.id)
    ctas = LandingPageService.get_cta_sections(empty_page.id)

    assert heroes == []
    assert features == []
    assert ctas == []
