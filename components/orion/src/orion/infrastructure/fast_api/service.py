import signal, sys, uvicorn
from fastapi import FastAPI
from typing import NoReturn

from orion.application.config.uvicorn import UvicornConfig
from orion.application.settings import app_logger
from orion.infrastructure.fast_api.api_routes import \
    include_root_routes, include_cluster_routes, include_auth_routes


# NOTE: Reused Code From other personal works, Take it as leverage rather tha
# a feature.

class Shutdown(Exception):
    """
    Custom exception class for handling graceful shutdown of the service.
    """
    def __init__(self):
        super(Shutdown, self).__init__()


def signal_term_handler(signal, frame):
    """
    Signal handler for terminating signals like SIGTERM and SIGQUIT.

    :param signal: Signal number.
    :param frame: Current stack frame.
    :raises Shutdown: Custom exception to initiate the shutdown process.
    """
    app_logger.info(f"SimpleFastAPIProfile - SIGTERM received, shutting down!")
    raise Shutdown


class SimpleFastAPIProfile:
    """
    Service profile to bootstrap and run the FastAPI application for the Miris
    API.

    This profile sets up a FastAPI application with specific configurations,
    mounts sub-applications, includes route handlers, and runs the application
    using Uvicorn.

    :param name: Name of the service profile.
    :type name: str
    """

    tags_metadata = []

    def __init__(
        self,
        settings: UvicornConfig,
    ):
        self.settings = settings
        title = "Orion Control Plane API"
        description = f"Exposed API Simulating the Qdrant Cloud API"
        version = "1.0"

        self.root_app = FastAPI(
            title=title,
            debug=False,
            description=description,
            version=version,
            docs_url=None,
            redoc_url="/docs",
        )
        fapi_app = FastAPI(
            title=title,
            debug=False,
            description=description,
            version=version,
            openapi_tags=self.tags_metadata,
            root_path="/api/v1",
            root_path_in_servers=False,
            openapi_url="/openapi.json",
            docs_url=None,
            redoc_url="/docs",
        )

        self.root_app.mount("/api/v1", fapi_app)

        include_root_routes(self.root_app)
        include_cluster_routes(fapi_app)
        include_auth_routes(fapi_app)

        fapi_app.setup()
        self.root_app.setup()

    def run(self) -> NoReturn:
        """
        Runs the FastAPI application using Uvicorn with specified
        configurations.

        Sets up signal handlers for graceful shutdown and logs application
        startup information. It handles keyboard interrupts and other
        exceptions during runtime.

        :raises Shutdown: On graceful shutdown of the service.
        :raises KeyboardInterrupt: On manual interruption.
        :raises Exception: For any other unhandled exceptions.
        """


        uvicorn_config: UvicornConfig = self.settings

        signal.signal(signal.SIGTERM, signal_term_handler)
        signal.signal(signal.SIGQUIT, signal_term_handler)

        inf_msg = f"Starting uvicorn: host {uvicorn_config.host}:" \
                  f"{uvicorn_config.port}, concurrency " \
                  f"{uvicorn_config.limit_concurrency}"
        app_logger.info(inf_msg)

        try:
            uvicorn.run(
                self.root_app,
                **uvicorn_config.as_dict()
            )
            raise Shutdown()
        except KeyboardInterrupt as e:
            sys.exit(-1)
        except Shutdown:
            sys.exit(0)
        except Exception as e:
            raise e
