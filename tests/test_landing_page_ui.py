"""UI smoke tests for landing page."""

import pytest
from app.database import reset_db
from app.landing_service import LandingPageService


@pytest.fixture()
def new_db():
    """Reset database for each test."""
    reset_db()
    yield
    reset_db()


def test_landing_page_service_integration(new_db):
    """Test that landing page service works correctly for UI integration."""
    # Test that sample data creation works
    landing_page = LandingPageService.create_sample_data()

    assert landing_page.id is not None
    assert landing_page.slug == "home"

    # Verify all components are created
    heroes = LandingPageService.get_hero_sections(landing_page.id)
    features = LandingPageService.get_features(landing_page.id)
    ctas = LandingPageService.get_cta_sections(landing_page.id)

    assert len(heroes) >= 1
    assert len(features) >= 3
    assert len(ctas) >= 1

    # Verify the landing page can be retrieved by slug
    retrieved_page = LandingPageService.get_active_landing_page("home")
    assert retrieved_page is not None
    assert retrieved_page.id == landing_page.id


def test_landing_page_ui_data_structure(new_db):
    """Test the data structure that the UI will consume."""
    # Create sample data
    landing_page = LandingPageService.create_sample_data()

    assert landing_page.id is not None

    # Test hero section data
    heroes = LandingPageService.get_hero_sections(landing_page.id)
    hero = heroes[0]
    assert hero.headline is not None
    assert hero.primary_button_text is not None
    assert hero.background_color is not None

    # Test features data
    features = LandingPageService.get_features(landing_page.id)
    featured_features = [f for f in features if f.is_featured]
    assert len(featured_features) >= 3

    for feature in featured_features:
        assert feature.title is not None
        assert feature.description is not None
        assert feature.icon is not None
        assert feature.icon_color is not None

    # Test CTA data
    ctas = LandingPageService.get_cta_sections(landing_page.id)
    cta = ctas[0]
    assert cta.headline is not None
    assert cta.primary_button_text is not None
    assert cta.primary_button_url is not None
