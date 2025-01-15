import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.staticfiles import StaticFiles

from app.core.config import Config
from app.presentation import api

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug('Startup Application')
    # await self._events_bus.start()
    yield
    # await self._events_bus.stop()
    logger.debug('Shutdown Application')


class FastAPIApp:
    def __init__(
        self,
        config: Config,
    ):
        self.app = FastAPI(
            title=config.app.title,
            description=config.app.description,
            version=config.app.version,
            debug=config.app.debug,
            openapi_url=config.app.openapi_url,
            docs_url=None,
            redoc_url=None,
            lifespan=lifespan,
        )
        config.app.app_id = id(self.app)
        self.config = config

    def set_static(self):
        """Настройка использования статических ресурсов"""

        self.app.mount('/static', StaticFiles(directory='static'), name='static')

        @self.app.get('/docs', include_in_schema=False)
        async def custom_swagger_ui_html():
            return get_swagger_ui_html(
                openapi_url=self.config.app.openapi_url,
                title=self.config.app.title,
                oauth2_redirect_url=self.app.swagger_ui_oauth2_redirect_url,
                swagger_js_url='/static/swagger-ui-bundle.js',
                swagger_css_url='/static/swagger-ui.css',
                swagger_favicon_url='/static/favicon.png',
                swagger_ui_parameters={'defaultModelsExpandDepth': -1},
            )

        @self.app.get(self.app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
        async def swagger_ui_redirect():
            return get_swagger_ui_oauth2_redirect_html()

        @self.app.get('/redoc', include_in_schema=False)
        async def redoc_html():
            return get_redoc_html(
                openapi_url=self.config.app.openapi_url,
                title=self.config.app.title,
                redoc_js_url='/static/redoc.standalone.js',
                redoc_favicon_url='/static/favicon.png',
                with_google_fonts=False,
            )

    def initialize(self) -> 'FastAPIApp':
        self.set_static()
        api.setup_handlers(self.app)
        api.setup_middlewares(self.app)
        self.app.include_router(api.router, prefix=self.config.app.api_url)
        return self
