"""Modern landing page UI module."""

import logging
from nicegui import ui
from typing import List
from app.landing_service import LandingPageService
from app.models import LandingPage, HeroSection, Feature, CallToActionSection

logger = logging.getLogger(__name__)


def apply_modern_theme():
    """Apply modern color theme for 2025."""
    ui.colors(
        primary="#2563eb",
        secondary="#64748b",
        accent="#10b981",
        positive="#10b981",
        negative="#ef4444",
        warning="#f59e0b",
        info="#3b82f6",
    )


def add_custom_styles():
    """Add custom CSS styles for the landing page."""
    ui.add_head_html("""
    <style>
        /* Import modern font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        
        /* Global styles */
        body {
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
        }
        
        /* Glass morphism effect */
        .glass-card {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        
        /* Gradient backgrounds */
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .gradient-text {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Smooth animations */
        .fade-in {
            animation: fadeIn 0.8s ease-in-out;
        }
        
        .slide-up {
            animation: slideUp 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        @keyframes slideUp {
            from { 
                opacity: 0;
                transform: translateY(30px);
            }
            to { 
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        /* Hover effects */
        .hover-lift:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
        }
        
        /* Feature card styling */
        .feature-card {
            transition: all 0.3s ease;
            border-radius: 16px;
        }
        
        .feature-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 24px rgba(0, 0, 0, 0.1);
        }
        
        /* Button enhancements */
        .cta-button {
            background: linear-gradient(45deg, #3b82f6 0%, #8b5cf6 100%);
            border: none;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            transition: all 0.3s ease;
        }
        
        .cta-button:hover {
            background: linear-gradient(45deg, #2563eb 0%, #7c3aed 100%);
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(59, 130, 246, 0.3);
        }
        
        /* Section spacing */
        .section-padding {
            padding: 5rem 0;
        }
        
        /* Responsive design helpers */
        @media (max-width: 768px) {
            .section-padding {
                padding: 3rem 0;
            }
        }
    </style>
    """)


def create_hero_section(hero: HeroSection):
    """Create a modern hero section."""
    # Hero background styling
    hero_bg_style = f"""
        background: {hero.background_color or "linear-gradient(135deg, #1e293b 0%, #334155 100%)"};
        color: {hero.text_color or "#ffffff"};
        min-height: 100vh;
        position: relative;
        overflow: hidden;
    """

    if hero.background_image_url:
        hero_bg_style += f"background-image: url('{hero.background_image_url}'); background-size: cover; background-position: center;"

    with ui.element("section").style(hero_bg_style).classes("flex items-center justify-center relative"):
        # Background decoration
        ui.element("div").style("""
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 30% 20%, rgba(59, 130, 246, 0.3) 0%, transparent 50%),
                        radial-gradient(circle at 70% 80%, rgba(139, 92, 246, 0.3) 0%, transparent 50%);
            pointer-events: none;
        """)

        # Hero content
        with ui.column().classes("z-10 max-w-4xl mx-auto text-center px-6 fade-in"):
            # Headline
            ui.label(hero.headline).classes("text-5xl md:text-6xl font-bold mb-6 leading-tight")

            # Subheadline
            if hero.subheadline:
                ui.label(hero.subheadline).classes("text-xl md:text-2xl font-light mb-8 opacity-90")

            # Description
            if hero.description:
                ui.label(hero.description).classes("text-lg mb-12 max-w-2xl mx-auto opacity-80 leading-relaxed")

            # Action buttons
            if hero.primary_button_text or hero.secondary_button_text:
                with ui.row().classes("gap-4 justify-center flex-wrap"):
                    if hero.primary_button_text:
                        primary_url = hero.primary_button_url or "#"

                        def handle_primary_click(url=primary_url):
                            if url != "#":
                                ui.navigate.to(url)

                        ui.button(hero.primary_button_text, on_click=handle_primary_click).classes(
                            "cta-button px-8 py-4 text-lg rounded-xl shadow-lg"
                        )

                    if hero.secondary_button_text:
                        secondary_url = hero.secondary_button_url or "#"

                        def handle_secondary_click(url=secondary_url):
                            if url != "#":
                                ui.navigate.to(url)

                        ui.button(hero.secondary_button_text, on_click=handle_secondary_click).classes(
                            "px-8 py-4 text-lg rounded-xl border-2 border-white/30 bg-transparent hover:bg-white/10 transition-all"
                        ).props("outline")


def create_feature_card(feature: Feature, is_featured: bool = False):
    """Create a modern feature card."""
    card_classes = "feature-card p-8 bg-white shadow-lg hover-lift transition-all duration-300"
    if is_featured:
        card_classes += " ring-2 ring-blue-500/20"

    with ui.card().classes(card_classes):
        # Feature icon
        if feature.icon:
            with ui.row().classes("items-center mb-6"):
                ui.icon(feature.icon, size="3rem").style(f"color: {feature.icon_color or '#3b82f6'}")
                if is_featured:
                    ui.badge("Featured").classes("ml-auto bg-gradient-to-r from-blue-500 to-purple-600 text-white")

        # Feature content
        ui.label(feature.title).classes("text-2xl font-bold mb-4 text-gray-800")
        ui.label(feature.description).classes("text-gray-600 leading-relaxed mb-6")

        # Feature link
        if feature.link_text and feature.link_url:
            ui.link(feature.link_text, feature.link_url, new_tab=True).classes(
                "text-blue-600 hover:text-blue-800 font-semibold inline-flex items-center"
            )


def create_features_section(features: List[Feature]):
    """Create the features section."""
    if not features:
        return

    with ui.element("section").classes("section-padding bg-gray-50"):
        with ui.column().classes("max-w-7xl mx-auto px-6"):
            # Section header
            with ui.column().classes("text-center mb-16 slide-up"):
                ui.label("Why Choose Our Platform?").classes("text-4xl font-bold text-gray-800 mb-4")
                ui.label("Discover the features that make us different").classes(
                    "text-xl text-gray-600 max-w-2xl mx-auto"
                )

            # Featured features (first 3)
            featured_features = [f for f in features if f.is_featured][:3]
            if featured_features:
                with ui.row().classes("gap-8 mb-16 justify-center flex-wrap"):
                    for feature in featured_features:
                        with ui.column().classes("w-full md:w-80"):
                            create_feature_card(feature, is_featured=True)

            # Additional features grid
            other_features = [f for f in features if not f.is_featured]
            if other_features:
                ui.label("More Features").classes("text-2xl font-bold text-center mb-8 text-gray-800")
                with ui.grid(columns=3).classes("gap-6 w-full"):
                    for feature in other_features:
                        create_feature_card(feature)


def create_cta_section(cta: CallToActionSection):
    """Create a call-to-action section."""
    # CTA styling
    cta_bg_style = f"""
        background: {cta.background_color or "linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)"};
        color: {cta.text_color or "#1f2937"};
    """

    if cta.background_image_url:
        cta_bg_style += (
            f"background-image: url('{cta.background_image_url}'); background-size: cover; background-position: center;"
        )

    with ui.element("section").style(cta_bg_style).classes("section-padding"):
        with ui.column().classes("max-w-4xl mx-auto text-center px-6 slide-up"):
            # CTA headline
            ui.label(cta.headline).classes("text-4xl md:text-5xl font-bold mb-6 text-gray-800")

            # CTA subheadline
            if cta.subheadline:
                ui.label(cta.subheadline).classes("text-xl font-medium mb-4 text-gray-700")

            # CTA description
            if cta.description:
                ui.label(cta.description).classes("text-lg mb-12 max-w-2xl mx-auto text-gray-600 leading-relaxed")

            # CTA buttons
            with ui.row().classes("gap-6 justify-center flex-wrap"):
                # Primary button
                primary_url = cta.primary_button_url

                def handle_cta_primary_click(url=primary_url):
                    ui.navigate.to(url)

                primary_btn = ui.button(cta.primary_button_text, on_click=handle_cta_primary_click)

                if cta.primary_button_style == "primary":
                    primary_btn.classes("cta-button px-10 py-4 text-lg rounded-xl shadow-lg")
                else:
                    primary_btn.classes("px-10 py-4 text-lg rounded-xl").props("outline")

                # Secondary button
                if cta.secondary_button_text and cta.secondary_button_url:
                    secondary_url = cta.secondary_button_url

                    def handle_cta_secondary_click(url=secondary_url):
                        ui.navigate.to(url)

                    secondary_btn = ui.button(cta.secondary_button_text, on_click=handle_cta_secondary_click)

                    if cta.secondary_button_style == "primary":
                        secondary_btn.classes("cta-button px-10 py-4 text-lg rounded-xl shadow-lg")
                    else:
                        secondary_btn.classes(
                            "px-10 py-4 text-lg rounded-xl border-2 border-gray-300 bg-white hover:bg-gray-50 text-gray-700 transition-all"
                        ).props("outline")


def create_landing_page_ui(landing_page: LandingPage):
    """Create the complete landing page UI."""
    if landing_page.id is None:
        ui.label("Landing page not found").classes("text-center text-xl text-red-600")
        return

    # Get page components
    hero_sections = LandingPageService.get_hero_sections(landing_page.id)
    features = LandingPageService.get_features(landing_page.id)
    cta_sections = LandingPageService.get_cta_sections(landing_page.id)

    # Set page metadata
    ui.add_head_html(f'''
        <title>{landing_page.meta_title or landing_page.title}</title>
        <meta name="description" content="{landing_page.meta_description or ""}">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    ''')

    # Hero sections
    for hero in hero_sections:
        create_hero_section(hero)

    # Features section
    if features:
        create_features_section(features)

    # CTA sections
    for cta in cta_sections:
        create_cta_section(cta)


def create():
    """Create the landing page module."""
    # Apply theme and styles
    apply_modern_theme()
    add_custom_styles()

    @ui.page("/")
    def landing_page():
        """Main landing page."""
        # Try to get existing landing page, create sample data if none exists
        page = LandingPageService.get_active_landing_page("home")

        if page is None:
            try:
                page = LandingPageService.create_sample_data()
                ui.notify("Sample landing page created!", type="info")
            except Exception as e:
                logger.error(f"Error creating sample landing page data: {str(e)}", exc_info=True)
                ui.label(f"Error creating landing page: {str(e)}").classes("text-center text-xl text-red-600 p-8")
                return

        create_landing_page_ui(page)
