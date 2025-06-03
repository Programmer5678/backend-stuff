from fastapi.staticfiles import StaticFiles
from application_instance import app
from engine_and_session import engine
from base_for_tables import Base

# Initialize database tables
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


#should prevent annoying caching - hope it doesnt fuck shit up though!

class NoCacheStaticFiles(StaticFiles):
    async def get_response(self, path, scope):
        response = await super().get_response(path, scope)
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

# Mount frontend files
app.mount("/", NoCacheStaticFiles(directory="../frontend", html=True), name="Frontend")
