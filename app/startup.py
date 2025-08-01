from app.database import create_tables
import app.landing_page


def startup() -> None:
    # this function is called before the first request
    create_tables()

    # Register landing page module
    app.landing_page.create()
