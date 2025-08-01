"""Tests for landing page service."""

import pytest
from app.database import reset_db
from app.landing_service import LandingPageService
from app.models import (
    LandingPageCreate,
    HeroSectionCreate,
    FeatureCreate,
    CallToActionSectionCreate,
)


@pytest.fixture()
def new_db():
    """Reset database for each test."""
    reset_db()
    yield
    reset_db()


def test_create_landing_page(new_db):
    """Test creating a new landing page."""
    data = LandingPageCreate(
        title="Test Landing Page",
        slug="test-page",
        meta_title="Test Page Title",
        meta_description="Test page description",
    )

    page = LandingPageService.create_landing_page(data)

    assert page.id is not None
    assert page.title == "Test Landing Page"
    assert page.slug == "test-page"
    assert page.meta_title == "Test Page Title"
    assert page.meta_description == "Test page description"
    assert page.is_active is True


def test_get_active_landing_page(new_db):
    """Test retrieving an active landing page."""
    # Create a landing page
    data = LandingPageCreate(
        title="Test Page",
        slug="test-slug",
    )
    created_page = LandingPageService.create_landing_page(data)

    # Retrieve it
    retrieved_page = LandingPageService.get_active_landing_page("test-slug")

    assert retrieved_page is not None
    assert retrieved_page.id == created_page.id
    assert retrieved_page.title == "Test Page"
    assert retrieved_page.slug == "test-slug"


def test_get_nonexistent_landing_page(new_db):
    """Test retrieving a non-existent landing page."""
    page = LandingPageService.get_active_landing_page("nonexistent")
    assert page is None


def test_create_hero_section(new_db):
    """Test creating a hero section."""
    # Create landing page first
    page_data = LandingPageCreate(title="Test Page", slug="test")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    hero_data = HeroSectionCreate(
        landing_page_id=page.id,
        headline="Test Headline",
        subheadline="Test Subheadline",
        description="Test description",
        primary_button_text="Click Me",
        primary_button_url="/test",
    )

    hero = LandingPageService.create_hero_section(hero_data)

    assert hero.id is not None
    assert hero.landing_page_id == page.id
    assert hero.headline == "Test Headline"
    assert hero.subheadline == "Test Subheadline"
    assert hero.description == "Test description"
    assert hero.primary_button_text == "Click Me"
    assert hero.primary_button_url == "/test"
    assert hero.is_active is True


def test_get_hero_sections(new_db):
    """Test retrieving hero sections for a landing page."""
    # Create landing page
    page_data = LandingPageCreate(title="Test Page", slug="test")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    # Create multiple hero sections
    hero1_data = HeroSectionCreate(
        landing_page_id=page.id,
        headline="First Hero",
        display_order=2,
    )
    hero2_data = HeroSectionCreate(
        landing_page_id=page.id,
        headline="Second Hero",
        display_order=1,
    )

    LandingPageService.create_hero_section(hero1_data)
    LandingPageService.create_hero_section(hero2_data)

    # Retrieve hero sections
    heroes = LandingPageService.get_hero_sections(page.id)

    assert len(heroes) == 2
    # Should be sorted by display_order (ascending)
    assert heroes[0].headline == "Second Hero"  # display_order=1
    assert heroes[1].headline == "First Hero"  # display_order=2


def test_create_feature(new_db):
    """Test creating a feature."""
    # Create landing page first
    page_data = LandingPageCreate(title="Test Page", slug="test")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    feature_data = FeatureCreate(
        landing_page_id=page.id,
        title="Test Feature",
        description="Test feature description",
        icon="star",
        is_featured=True,
    )

    feature = LandingPageService.create_feature(feature_data)

    assert feature.id is not None
    assert feature.landing_page_id == page.id
    assert feature.title == "Test Feature"
    assert feature.description == "Test feature description"
    assert feature.icon == "star"
    assert feature.is_featured is True
    assert feature.is_active is True


def test_get_features(new_db):
    """Test retrieving features for a landing page."""
    # Create landing page
    page_data = LandingPageCreate(title="Test Page", slug="test")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    # Create multiple features
    feature1_data = FeatureCreate(
        landing_page_id=page.id,
        title="Feature B",
        description="Description B",
        display_order=2,
    )
    feature2_data = FeatureCreate(
        landing_page_id=page.id,
        title="Feature A",
        description="Description A",
        display_order=1,
    )

    LandingPageService.create_feature(feature1_data)
    LandingPageService.create_feature(feature2_data)

    # Retrieve features
    features = LandingPageService.get_features(page.id)

    assert len(features) == 2
    # Should be sorted by display_order, then title
    assert features[0].title == "Feature A"
    assert features[1].title == "Feature B"


def test_create_cta_section(new_db):
    """Test creating a CTA section."""
    # Create landing page first
    page_data = LandingPageCreate(title="Test Page", slug="test")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    cta_data = CallToActionSectionCreate(
        landing_page_id=page.id,
        headline="Test CTA",
        subheadline="Test CTA Subheadline",
        description="Test CTA description",
        primary_button_text="Primary Action",
        primary_button_url="/primary",
        secondary_button_text="Secondary Action",
        secondary_button_url="/secondary",
    )

    cta = LandingPageService.create_cta_section(cta_data)

    assert cta.id is not None
    assert cta.landing_page_id == page.id
    assert cta.headline == "Test CTA"
    assert cta.subheadline == "Test CTA Subheadline"
    assert cta.description == "Test CTA description"
    assert cta.primary_button_text == "Primary Action"
    assert cta.primary_button_url == "/primary"
    assert cta.secondary_button_text == "Secondary Action"
    assert cta.secondary_button_url == "/secondary"
    assert cta.is_active is True


def test_get_cta_sections(new_db):
    """Test retrieving CTA sections for a landing page."""
    # Create landing page
    page_data = LandingPageCreate(title="Test Page", slug="test")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    # Create multiple CTA sections
    cta1_data = CallToActionSectionCreate(
        landing_page_id=page.id,
        headline="First CTA",
        primary_button_text="Action 1",
        primary_button_url="/action1",
        display_order=2,
    )
    cta2_data = CallToActionSectionCreate(
        landing_page_id=page.id,
        headline="Second CTA",
        primary_button_text="Action 2",
        primary_button_url="/action2",
        display_order=1,
    )

    LandingPageService.create_cta_section(cta1_data)
    LandingPageService.create_cta_section(cta2_data)

    # Retrieve CTA sections
    ctas = LandingPageService.get_cta_sections(page.id)

    assert len(ctas) == 2
    # Should be sorted by display_order (ascending)
    assert ctas[0].headline == "Second CTA"  # display_order=1
    assert ctas[1].headline == "First CTA"  # display_order=2


def test_create_sample_data(new_db):
    """Test creating sample landing page data."""
    landing_page = LandingPageService.create_sample_data()

    assert landing_page.id is not None
    assert landing_page.title == "Modern Landing Page"
    assert landing_page.slug == "home"

    # Verify components were created
    heroes = LandingPageService.get_hero_sections(landing_page.id)
    assert len(heroes) >= 1
    assert "Transform Your Business" in heroes[0].headline

    features = LandingPageService.get_features(landing_page.id)
    assert len(features) >= 3

    ctas = LandingPageService.get_cta_sections(landing_page.id)
    assert len(ctas) >= 1
    assert "Ready to Transform" in ctas[0].headline


def test_get_empty_components(new_db):
    """Test retrieving components for landing page with no components."""
    # Create landing page only
    page_data = LandingPageCreate(title="Empty Page", slug="empty")
    page = LandingPageService.create_landing_page(page_data)

    assert page.id is not None

    # Should return empty lists
    heroes = LandingPageService.get_hero_sections(page.id)
    features = LandingPageService.get_features(page.id)
    ctas = LandingPageService.get_cta_sections(page.id)

    assert heroes == []
    assert features == []
    assert ctas == []


def test_get_components_for_nonexistent_page(new_db):
    """Test retrieving components for non-existent landing page."""
    heroes = LandingPageService.get_hero_sections(999)
    features = LandingPageService.get_features(999)
    ctas = LandingPageService.get_cta_sections(999)

    assert heroes == []
    assert features == []
    assert ctas == []
