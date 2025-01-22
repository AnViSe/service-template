from app.main import setup_fastapi, setup_faststream

fastapi_app = setup_fastapi()
# faststream_app = setup_faststream()

# bus = faststream_app.app
http = fastapi_app.app
