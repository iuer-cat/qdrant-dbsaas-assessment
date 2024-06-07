from fastapi import APIRouter

from orion.infrastructure.fast_api.models.responses.v1.health_check import \
    HealthCheckResponse

main_router = APIRouter(
    prefix="/health_check",
    tags=["operations"],
)


@main_router.get("", response_model=HealthCheckResponse)
async def health_check():
    """
    Endpoint used by a load balancer to ensure that the application is ready to
    receive traffic.

    This endpoint is a health check, typically used in production environments
    to verify that an application instance is operational and can handle
    requests. It's commonly polled by load balancers or monitoring systems
    to determine service status.
    """
    return HealthCheckResponse()
