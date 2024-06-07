from datetime import datetime
from fastapi import Path

from orion.application.services.auth.endpoint import DBClusterEndpointService
from orion.application.services.db_cluster.claim_provision import \
    DbClusterProvisionerService
from orion.application.settings import app_logger

from orion.domain.value_objects.resource_claim import ResourceClaim
from orion.infrastructure.fast_api.models.requests.v1.accounts.clusters.cluster import \
    CreateClusterBodyRequest
from orion.infrastructure.fast_api.models.responses.v1.accounts.clusters.cluster import \
    CreateClusterResponse
from orion.infrastructure.fast_api.routers.v1 import accounts_router_v1
from orion.infrastructure.repositories.resource_map import \
    YamlCloudProviderRepository


@accounts_router_v1.post("/{account_id}/clusters",
                response_model=CreateClusterResponse,
                tags=["Create Cluster"],
                status_code=202,
                operation_id="create_cluster"
                )
async def create_cluster(
        parameters: CreateClusterBodyRequest,
        account_id: str = Path(description="Organization Account ID"),
) -> CreateClusterResponse:
    # Not Implemented: Based on account_id validate the account is eligible for
    # new clusters and is not deactivate.

    claim = ResourceClaim(
        cloud_provider=parameters.cloud_provider,
        cloud_region=parameters.cloud_region,
        num_nodes=parameters.configuration.num_nodes,
        disk=parameters.configuration.node_configuration.disk,
        memory=parameters.configuration.node_configuration.memory,
        cpu=parameters.configuration.node_configuration.cpu,
    )

    app_logger.info(f"New Cluster Creation request, Claim: {claim.as_dict()}")

    resources_repository = YamlCloudProviderRepository()
    claim_provisioner = DbClusterProvisionerService(resources_repository)
    resource_allocation = claim_provisioner.allocate_resources(claim)

    endpoint_service = DBClusterEndpointService(
        cluster_name=parameters.name,
        cloud_region=parameters.cloud_region,
        cloud_provider=parameters.cloud_provider,
        account_id=account_id,
    )
    fqdn = endpoint_service.register()

    app_logger.info(f"Generated Endpoint: {fqdn}, for {account_id} and "
                     f"cluster: {parameters.name}")

    command = claim_provisioner.claim_provision(
        cluster_name=parameters.name,
        cluster_endpoint=fqdn,
        account_id=account_id,
        claim=claim,
        resource_allocation=resource_allocation
    )

    # Not Implemented: The cluster request must be persisted amd some fields
    # related to the db-cluster state might be addded should: IN_CREATION,
    # PROVISIONED, FAILED, FROZEN, MAINTENANCE...
    return CreateClusterResponse(
        id=command.id,
        created_at=datetime.utcnow(),
        name=command.name,
        cloud_provider=command.cloud_provider,
        cloud_region=command.cloud_region,
        endpoint=fqdn
    )