import logging.config

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from application.settings.app import Settings as app_settings
from application.settings.db import Settings as db_settings
from application.settings.auth import Settings as Auth_settings
from application.settings.logger import settings, config
from controllers.dependencies import get_session, get_user_service, oauth2_scheme

from controllers.routers.v1.routers import router
from middleware.cors import get_cors_middleware
from services.user import UserService

app_settings = app_settings()
auth_settings = Auth_settings()
db_url = db_settings().get_db_url()
logger_settings = settings.Settings()


def setup_dependencies(app: FastAPI) -> None:
    engine = create_async_engine(db_url)
    session = async_sessionmaker(engine, expire_on_commit=False)
    app.dependency_overrides[async_sessionmaker] = lambda: session
    app.dependency_overrides[Auth_settings] = lambda: auth_settings
    app.dependency_overrides[AsyncSession] = get_session
    app.dependency_overrides[UserService] = get_user_service
    app.dependency_overrides[OAuth2PasswordBearer] = oauth2_scheme


def app_setup(app: FastAPI) -> None:
    setup_dependencies(app)


def init_app() -> FastAPI:
    log_config = config.make_logger_conf(logger_settings.log_config)
    if not app_settings.DEBUG:
        logging.config.dictConfig(log_config)
    app = FastAPI(
        title="UberPopug SSO Service",
        description="Сервис авторизации и аутентификации для попугов",
        debug=app_settings.DEBUG,
        middleware=[get_cors_middleware(app_settings.CORS_ORIGINS)],
    )
    app.include_router(router)
    app_setup(app)
    return app
