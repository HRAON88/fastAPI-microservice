import logging

from fastapi import FastAPI
from uvicorn import run

from app.endpoints import list_of_routes


def bind_routes(application: FastAPI) -> None:
    """
    Bind all routes to application.
    """
    for route in list_of_routes:
        application.include_router(route)


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """
    application = FastAPI(
        title="Server",
        version="1.0.0",
    )
    bind_routes(application)
    return application


app = get_app()

if __name__ == "__main__":
    logging.info('парсер запускается')
    run(
        "app.__main__:app",
        reload=True,
        reload_dirs=["app"],
        port=8002,
        log_level="debug",
        workers=1,
    )
    logging.info('парсер выключен')
