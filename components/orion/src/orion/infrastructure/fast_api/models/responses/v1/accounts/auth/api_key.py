from datetime import datetime
from pydantic import BaseModel, Field


class CreateAPiKeyResponse(BaseModel):
    """
    Pydantic model response when api-key is created.
    """

    id: str = Field(description="Unique API-KEY ID")
    account_id: str = Field(description="Account ID owner of the API-KEY")
    created_at: datetime = Field(description="Creation date")
    db_cluster_id: str = Field(description="Qdrant DB Cluster associated to the api-key")
    api_key: str = Field(description="The Salt Hashing api-key generated")