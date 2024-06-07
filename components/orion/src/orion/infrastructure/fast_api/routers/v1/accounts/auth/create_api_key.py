import uuid
from datetime import datetime
from fastapi import Path

from nexus.core.infrastructure.repositories.db_cluster import \
    YamlDBClusterRepository
from orion.application.services.auth.api_key import DBaaSApiKeyService
from orion.application.settings import app_logger
from orion.infrastructure.fast_api.models.requests.v1.accounts.auth.api_key import \
    CreateApiKeyBodyRequest
from orion.infrastructure.fast_api.models.responses.v1.accounts.auth.api_key import \
    CreateAPiKeyResponse
from orion.infrastructure.fast_api.routers.v1 import accounts_router_v1


@accounts_router_v1.post("/{account_id}/auth/api-keys",
                response_model=CreateAPiKeyResponse,
                tags=["Create Api Keys"],
                status_code=201,
                operation_id="create_api_key"
                )
async def create_cluster(
        parameters: CreateApiKeyBodyRequest,
        account_id: str = Path(description="Organization Account ID"),
) -> CreateAPiKeyResponse:
    # Not Implemented: Based on account_id validate the account is eligible for
    # new clusters and is not deactivate.

    app_logger.info(f"New Api-key Creation request, Claim: "
                    f"{parameters.model_dump()}")

    db_cluster_repository = YamlDBClusterRepository()

    db_cluster_repository = DBaaSApiKeyService(
        db_cluster_repository=db_cluster_repository
    )
    cluster_api_key = db_cluster_repository.create_api_key(
        db_cluster_id=parameters.db_cluster_id)

    app_logger.info(f"New Api-key Created {cluster_api_key[:5]} "
                    f"for cluster {parameters.db_cluster_id} "
                    f"account: {account_id}")

    return CreateAPiKeyResponse(
        id=str(uuid.uuid4()),  # New UUID for each new api-key
        created_at=datetime.utcnow(),
        account_id=account_id,
        db_cluster_id=parameters.db_cluster_id,
        api_key=cluster_api_key,
    )