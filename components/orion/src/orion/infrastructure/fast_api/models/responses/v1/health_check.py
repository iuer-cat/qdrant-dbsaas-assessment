from pydantic import BaseModel, Field


class HealthCheckResponse(BaseModel):
    """
    Used primarily to inform the load balancer that the service is ready to
    handle requests.
    """

    message: str = Field(
        description="Message informing the status of the service",
        default="Service up and running"
    )








