from app.main import setup_fastapi

fastapi_app = setup_fastapi()

http = fastapi_app.app
