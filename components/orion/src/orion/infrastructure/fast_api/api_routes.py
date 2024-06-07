from typing import NoReturn
from fastapi import FastAPI

from orion.infrastructure.fast_api.routers.v1 import health_check
from orion.infrastructure.fast_api.routers.v1.accounts.clusters import \
    create_cluster
from orion.infrastructure.fast_api.routers.v1.accounts.auth import \
    create_api_key


def include_root_routes(root_api: FastAPI) -> NoReturn:
    """
    Includes general and administrative endpoints, such as health checks,
    into the root FastAPI application.

    :param root_api: The root FastAPI application instance.
    :type root_api: FastAPI
    :rtype: NoReturn
    """

    root_api.include_router(health_check.main_router)


def include_cluster_routes(
        fapi_app: FastAPI
) -> NoReturn:
    """
    Includes routes and endpoints for the management of Qdrant DB Clusters.

    :param fapi_app: The FastAPI application instance.
    :type fapi_app: FastAPI
    :rtype: NoReturn
    """

    fapi_app.include_router(create_cluster.accounts_router_v1)


def include_auth_routes(
        fapi_app: FastAPI
) -> NoReturn:
    """
    Includes routes and endpoints for the management of GateKeeper API keys.

    :param fapi_app: The FastAPI application instance.
    :type fapi_app: FastAPI
    :rtype: NoReturn
    """

    fapi_app.include_router(create_api_key.accounts_router_v1)

