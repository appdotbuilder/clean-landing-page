"""Service layer for landing page management."""

from typing import List, Optional
from sqlmodel import select, and_, asc
from app.database import get_session
from app.models import (
    LandingPage,
    HeroSection,
    Feature,
    CallToActionSection,
    LandingPageTheme,
    LandingPageCreate,
    HeroSectionCreate,
    FeatureCreate,
    CallToActionSectionCreate,
)


class LandingPageService:
    """Service for managing landing pages and their components."""

    @staticmethod
    def get_active_landing_page(slug: str = "home") -> Optional[LandingPage]:
        """Get an active landing page by slug."""
        with get_session() as session:
            statement = select(LandingPage).where(and_(LandingPage.slug == slug, LandingPage.is_active))
            return session.exec(statement).first()

    @staticmethod
    def get_hero_sections(landing_page_id: int) -> List[HeroSection]:
        """Get active hero sections for a landing page, sorted by display order."""
        with get_session() as session:
            statement = (
                select(HeroSection)
                .where(
                    and_(
                        HeroSection.landing_page_id == landing_page_id,
                        HeroSection.is_active,
                    )
                )
                .order_by(asc(HeroSection.display_order))
            )
            return list(session.exec(statement).all())

    @staticmethod
    def get_features(landing_page_id: int) -> List[Feature]:
        """Get active features for a landing page, sorted by display order."""
        with get_session() as session:
            statement = (
                select(Feature)
                .where(
                    and_(
                        Feature.landing_page_id == landing_page_id,
                        Feature.is_active,
                    )
                )
                .order_by(asc(Feature.display_order), asc(Feature.title))
            )
            return list(session.exec(statement).all())

    @staticmethod
    def get_cta_sections(landing_page_id: int) -> List[CallToActionSection]:
        """Get active CTA sections for a landing page, sorted by display order."""
        with get_session() as session:
            statement = (
                select(CallToActionSection)
                .where(
                    and_(
                        CallToActionSection.landing_page_id == landing_page_id,
                        CallToActionSection.is_active,
                    )
                )
                .order_by(asc(CallToActionSection.display_order))
            )
            return list(session.exec(statement).all())

    @staticmethod
    def create_landing_page(data: LandingPageCreate) -> LandingPage:
        """Create a new landing page."""
        with get_session() as session:
            landing_page = LandingPage(**data.model_dump())
            session.add(landing_page)
            session.commit()
            session.refresh(landing_page)
            return landing_page

    @staticmethod
    def create_hero_section(data: HeroSectionCreate) -> HeroSection:
        """Create a new hero section."""
        with get_session() as session:
            hero_section = HeroSection(**data.model_dump())
            session.add(hero_section)
            session.commit()
            session.refresh(hero_section)
            return hero_section

    @staticmethod
    def create_feature(data: FeatureCreate) -> Feature:
        """Create a new feature."""
        with get_session() as session:
            feature = Feature(**data.model_dump())
            session.add(feature)
            session.commit()
            session.refresh(feature)
            return feature

    @staticmethod
    def create_cta_section(data: CallToActionSectionCreate) -> CallToActionSection:
        """Create a new CTA section."""
        with get_session() as session:
            cta_section = CallToActionSection(**data.model_dump())
            session.add(cta_section)
            session.commit()
            session.refresh(cta_section)
            return cta_section

    @staticmethod
    def get_theme(name: str = "default") -> Optional[LandingPageTheme]:
        """Get a theme by name."""
        with get_session() as session:
            statement = select(LandingPageTheme).where(
                and_(
                    LandingPageTheme.name == name,
                    LandingPageTheme.is_active,
                )
            )
            return session.exec(statement).first()

    @staticmethod
    def create_sample_data() -> LandingPage:
        """Create sample landing page data for demonstration."""
        # Create landing page
        landing_page_data = LandingPageCreate(
            title="Modern Landing Page",
            slug="home",
            meta_title="Modern Landing Page - Beautiful Design",
            meta_description="A modern and elegant landing page with clean design and engaging features.",
        )
        landing_page = LandingPageService.create_landing_page(landing_page_data)

        if landing_page.id is None:
            raise ValueError("Landing page creation failed")

        # Create hero section
        hero_data = HeroSectionCreate(
            landing_page_id=landing_page.id,
            headline="Transform Your Business with Modern Solutions",
            subheadline="Unlock your potential with our cutting-edge platform",
            description="Experience the future of business automation with our intuitive, powerful, and beautifully designed platform that grows with your needs.",
            background_color="#1e293b",
            text_color="#ffffff",
            primary_button_text="Get Started",
            primary_button_url="/signup",
            alignment="center",
            height="full",
        )
        LandingPageService.create_hero_section(hero_data)

        # Create features
        features_data = [
            FeatureCreate(
                landing_page_id=landing_page.id,
                title="Lightning Fast Performance",
                description="Built with modern technology stack for maximum speed and reliability. Experience blazing-fast load times and seamless user interactions.",
                icon="speed",
                icon_color="#10b981",
                display_order=1,
                is_featured=True,
            ),
            FeatureCreate(
                landing_page_id=landing_page.id,
                title="Intuitive Design",
                description="User-centered design that makes complex tasks simple. Our interface adapts to your workflow, not the other way around.",
                icon="design_services",
                icon_color="#3b82f6",
                display_order=2,
                is_featured=True,
            ),
            FeatureCreate(
                landing_page_id=landing_page.id,
                title="Enterprise Security",
                description="Bank-level security with end-to-end encryption, SSO integration, and compliance with industry standards.",
                icon="security",
                icon_color="#8b5cf6",
                display_order=3,
                is_featured=True,
            ),
            FeatureCreate(
                landing_page_id=landing_page.id,
                title="24/7 Support",
                description="Our dedicated support team is available around the clock to help you succeed with personalized assistance.",
                icon="support_agent",
                icon_color="#f59e0b",
                display_order=4,
            ),
            FeatureCreate(
                landing_page_id=landing_page.id,
                title="Scalable Infrastructure",
                description="From startup to enterprise, our platform scales with your business without compromising performance.",
                icon="trending_up",
                icon_color="#ef4444",
                display_order=5,
            ),
            FeatureCreate(
                landing_page_id=landing_page.id,
                title="Advanced Analytics",
                description="Make data-driven decisions with comprehensive analytics and real-time insights into your business metrics.",
                icon="analytics",
                icon_color="#06b6d4",
                display_order=6,
            ),
        ]

        for feature_data in features_data:
            LandingPageService.create_feature(feature_data)

        # Create CTA section
        cta_data = CallToActionSectionCreate(
            landing_page_id=landing_page.id,
            headline="Ready to Transform Your Business?",
            subheadline="Join thousands of satisfied customers",
            description="Start your journey today with our free trial. No credit card required, no hidden fees, just pure innovation at your fingertips.",
            primary_button_text="Start Free Trial",
            primary_button_url="/trial",
            secondary_button_text="View Pricing",
            secondary_button_url="/pricing",
            background_color="#f8fafc",
            alignment="center",
            size="large",
        )
        LandingPageService.create_cta_section(cta_data)

        return landing_page
