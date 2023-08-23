import logging.config

from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer

from billing.src.middleware.cors import get_cors_middleware
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from billing.src.application.settings.app import Settings as App_settings
from billing.src.application.settings.auth import Settings as Auth_settings
from billing.src.application.settings.broker import Settings as Broker_settings
from billing.src.application.settings.db import Settings as DB_settings
from billing.src.application.settings.logger import config, settings
from billing.src.controllers.dependencies import get_session, get_billing_service, oauth2_scheme
from billing.src.controllers.routers.v1.routers import router
from billing.src.services.billing import BillingService

app_settings = App_settings()
auth_settings = Auth_settings()
db_url = DB_settings().get_db_url()
logger_settings = settings.Settings()
broker_settings = Broker_settings()

engine = create_async_engine(db_url)
session = async_sessionmaker(engine, expire_on_commit=False)


def setup_dependencies(app: FastAPI) -> None:
    app.dependency_overrides[async_sessionmaker] = lambda: session
    app.dependency_overrides[Auth_settings] = lambda: auth_settings
    app.dependency_overrides[Broker_settings] = lambda: broker_settings
    app.dependency_overrides[AsyncSession] = get_session
    app.dependency_overrides[OAuth2PasswordBearer] = oauth2_scheme
    app.dependency_overrides[BillingService] = get_billing_service


def app_setup(app: FastAPI) -> None:
    setup_dependencies(app)


def init_app() -> FastAPI:
    log_config = config.make_logger_conf(logger_settings.log_config)
    if not app_settings.DEBUG:
        logging.config.dictConfig(log_config)
    app = FastAPI(
        title="UberPopug Billing Service",
        description="Сервис аккаунтинга/биллинга для попугов",
        debug=app_settings.DEBUG,
        middleware=[get_cors_middleware(app_settings.CORS_ORIGINS)],
    )
    app.include_router(router)
    app_setup(app)
    return app
