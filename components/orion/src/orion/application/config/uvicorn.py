from nexus.core.infrastructure.model.implementations import ConfigModel


class UvicornConfig(ConfigModel):
    """
    The Orion API uvicorn configuration model.
    """

    host: str = '0.0.0.0'
    port: int = 8080
    log_level: str = 'error'
    loop: str = 'uvloop'
    interface: str = 'asgi3'
    limit_concurrency: int = 100
    timeout_keep_alive: int = 60
    timeout_graceful_shutdown: int = 60
