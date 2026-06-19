
from quart import Quart
from quart_cors import cors
from app.api.streams import streams_bp

def create_app():
    app=Quart(__name__)
    app=cors(app,allow_origin="*")
    app.register_blueprint(streams_bp,url_prefix="/api/v1/streams")

    @app.get("/health")
    async def health():
        return {"status":"UP"}

    return app
