from fastapi.staticfiles import StaticFiles
from application_instance import app
from engine_and_session import engine
from base_for_tables import Base

# Initialize database tables
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

# Mount frontend files
app.mount("/joey", StaticFiles(directory="../frontend", html=True), name="Frontend")

