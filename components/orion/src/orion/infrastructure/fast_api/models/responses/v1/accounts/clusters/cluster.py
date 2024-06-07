from datetime import datetime
from pydantic import BaseModel, Field


class CreateClusterResponse(BaseModel):
    """
    Pydantic model response for a Qdrant DB cluster created.

    """

    id: str = Field(description="Unique Qdrant DB Cluster Identifier")
    created_at: datetime = Field(description="Creation date")
    name: str = Field(description="Unique Qdrant DB Cluster Common Name")
    cloud_provider: str = Field(description="Cloud provider used for the provision")
    cloud_region: str = Field(description="Cloud provider region used for the provision")
    endpoint: str = Field(description="HTTP and HTTPS endpoint where the Qdrant "
                                      "DB cluster is available")

