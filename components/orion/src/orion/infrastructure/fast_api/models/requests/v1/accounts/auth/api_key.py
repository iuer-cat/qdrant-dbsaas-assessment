from pydantic import BaseModel, Field


class CreateApiKeyBodyRequest(BaseModel):
    """
    Pydantic model for creating an API key request.
    """

    class Config:
        extra = "forbid"

    db_cluster_id: str = Field(description="Unique identifier for a existent "
                                           "Qdrant DB Cluster")
