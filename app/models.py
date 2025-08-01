from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from datetime import datetime
from typing import Optional, List, Dict, Any

# Landing Page Models


class LandingPage(SQLModel, table=True):
    """Main landing page configuration."""

    __tablename__ = "landing_pages"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=200)
    slug: str = Field(unique=True, max_length=100, description="URL-friendly identifier")
    is_active: bool = Field(default=True)
    meta_title: Optional[str] = Field(default=None, max_length=200)
    meta_description: Optional[str] = Field(default=None, max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    hero_sections: List["HeroSection"] = Relationship(back_populates="landing_page")
    features: List["Feature"] = Relationship(back_populates="landing_page")
    cta_sections: List["CallToActionSection"] = Relationship(back_populates="landing_page")


class HeroSection(SQLModel, table=True):
    """Hero section content for landing pages."""

    __tablename__ = "hero_sections"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    landing_page_id: int = Field(foreign_key="landing_pages.id")

    # Content fields
    headline: str = Field(max_length=300)
    subheadline: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Visual elements
    background_image_url: Optional[str] = Field(default=None, max_length=500)
    background_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")
    text_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")

    # Call-to-action button
    primary_button_text: Optional[str] = Field(default=None, max_length=100)
    primary_button_url: Optional[str] = Field(default=None, max_length=500)
    secondary_button_text: Optional[str] = Field(default=None, max_length=100)
    secondary_button_url: Optional[str] = Field(default=None, max_length=500)

    # Layout and styling
    alignment: str = Field(default="center", max_length=20, description="left, center, right")
    height: str = Field(default="full", max_length=20, description="full, medium, compact")

    # Ordering
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    landing_page: LandingPage = Relationship(back_populates="hero_sections")


class Feature(SQLModel, table=True):
    """Feature highlight for landing pages."""

    __tablename__ = "features"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    landing_page_id: int = Field(foreign_key="landing_pages.id")

    # Content fields
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)

    # Visual elements
    icon: Optional[str] = Field(default=None, max_length=100, description="Icon name or CSS class")
    icon_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")
    image_url: Optional[str] = Field(default=None, max_length=500)

    # Links and actions
    link_text: Optional[str] = Field(default=None, max_length=100)
    link_url: Optional[str] = Field(default=None, max_length=500)

    # Layout and styling
    background_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")
    text_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")

    # Ordering and display
    display_order: int = Field(default=0)
    is_featured: bool = Field(default=False, description="Highlight this feature")
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    landing_page: LandingPage = Relationship(back_populates="features")


class CallToActionSection(SQLModel, table=True):
    """Call-to-action section for landing pages."""

    __tablename__ = "cta_sections"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    landing_page_id: int = Field(foreign_key="landing_pages.id")

    # Content fields
    headline: str = Field(max_length=300)
    subheadline: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None, max_length=1000)

    # Primary CTA
    primary_button_text: str = Field(max_length=100)
    primary_button_url: str = Field(max_length=500)
    primary_button_style: str = Field(default="primary", max_length=50, description="primary, secondary, outline")

    # Secondary CTA (optional)
    secondary_button_text: Optional[str] = Field(default=None, max_length=100)
    secondary_button_url: Optional[str] = Field(default=None, max_length=500)
    secondary_button_style: str = Field(default="secondary", max_length=50)

    # Visual design
    background_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")
    text_color: Optional[str] = Field(default=None, max_length=50, description="CSS color value")
    background_image_url: Optional[str] = Field(default=None, max_length=500)

    # Layout
    alignment: str = Field(default="center", max_length=20, description="left, center, right")
    size: str = Field(default="medium", max_length=20, description="small, medium, large")

    # Ordering and display
    display_order: int = Field(default=0)
    is_active: bool = Field(default=True)

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    landing_page: LandingPage = Relationship(back_populates="cta_sections")


class LandingPageTheme(SQLModel, table=True):
    """Theme configuration for landing pages."""

    __tablename__ = "landing_page_themes"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100, unique=True)
    description: Optional[str] = Field(default=None, max_length=500)

    # Color scheme
    primary_color: str = Field(max_length=50, description="Primary brand color")
    secondary_color: str = Field(max_length=50, description="Secondary brand color")
    accent_color: str = Field(max_length=50, description="Accent color for highlights")
    background_color: str = Field(default="#ffffff", max_length=50)
    text_color: str = Field(default="#333333", max_length=50)

    # Typography
    font_family: str = Field(default="Inter, sans-serif", max_length=200)
    heading_font_family: Optional[str] = Field(default=None, max_length=200)

    # Spacing and layout
    border_radius: str = Field(default="8px", max_length=50, description="Default border radius")
    spacing_unit: str = Field(default="1rem", max_length=50, description="Base spacing unit")

    # Additional styling options
    custom_css: Optional[str] = Field(default=None, description="Custom CSS overrides")
    design_tokens: Dict[str, Any] = Field(default={}, sa_column=Column(JSON), description="Additional design tokens")

    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Non-persistent schemas for validation and API responses


class LandingPageCreate(SQLModel, table=False):
    """Schema for creating a new landing page."""

    title: str = Field(max_length=200)
    slug: str = Field(max_length=100)
    meta_title: Optional[str] = Field(default=None, max_length=200)
    meta_description: Optional[str] = Field(default=None, max_length=500)


class LandingPageUpdate(SQLModel, table=False):
    """Schema for updating a landing page."""

    title: Optional[str] = Field(default=None, max_length=200)
    slug: Optional[str] = Field(default=None, max_length=100)
    is_active: Optional[bool] = Field(default=None)
    meta_title: Optional[str] = Field(default=None, max_length=200)
    meta_description: Optional[str] = Field(default=None, max_length=500)


class HeroSectionCreate(SQLModel, table=False):
    """Schema for creating a hero section."""

    landing_page_id: int
    headline: str = Field(max_length=300)
    subheadline: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None, max_length=1000)
    background_image_url: Optional[str] = Field(default=None, max_length=500)
    primary_button_text: Optional[str] = Field(default=None, max_length=100)
    primary_button_url: Optional[str] = Field(default=None, max_length=500)
    alignment: str = Field(default="center", max_length=20)


class FeatureCreate(SQLModel, table=False):
    """Schema for creating a feature."""

    landing_page_id: int
    title: str = Field(max_length=200)
    description: str = Field(max_length=1000)
    icon: Optional[str] = Field(default=None, max_length=100)
    image_url: Optional[str] = Field(default=None, max_length=500)
    link_text: Optional[str] = Field(default=None, max_length=100)
    link_url: Optional[str] = Field(default=None, max_length=500)
    is_featured: bool = Field(default=False)


class CallToActionSectionCreate(SQLModel, table=False):
    """Schema for creating a call-to-action section."""

    landing_page_id: int
    headline: str = Field(max_length=300)
    subheadline: Optional[str] = Field(default=None, max_length=500)
    description: Optional[str] = Field(default=None, max_length=1000)
    primary_button_text: str = Field(max_length=100)
    primary_button_url: str = Field(max_length=500)
    secondary_button_text: Optional[str] = Field(default=None, max_length=100)
    secondary_button_url: Optional[str] = Field(default=None, max_length=500)
    alignment: str = Field(default="center", max_length=20)


class LandingPageThemeCreate(SQLModel, table=False):
    """Schema for creating a landing page theme."""

    name: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    primary_color: str = Field(max_length=50)
    secondary_color: str = Field(max_length=50)
    accent_color: str = Field(max_length=50)
    font_family: str = Field(default="Inter, sans-serif", max_length=200)
