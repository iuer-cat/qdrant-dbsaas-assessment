import uuid
from datetime import datetime
from typing import NoReturn


from nexus.command_bus.application.command_bus import CommandBus
from nexus.command_bus.domain.commands.v1.db_clusters.models import \
    DBClusterConfiguration, DBNodeSpecs
from nexus.command_bus.domain.commands.v1.db_clusters.provision import \
    ProvisionDBCluster
from orion.application.settings import app_logger

from orion.domain.entities.resource_allocation import ResourceAllocation
from orion.domain.ports import CloudProviderReadModelRepository
from orion.domain.value_objects.resource_claim import ResourceClaim


class DbClusterProvisionerService:
    """
    This Application Service is the entry point for provisioning a new Qdrant DB
    Cluster.

    The service generates a configuration and a resource claim, which is
    evaluated by the aggregate responsible for resource allocation, the
    CloudProviderResourceMap. If the allocation is successful, a
    ProvisionDBCluster command is generated, which will eventually be consumed
    by the Nebula component for provisioning the actual infrastructure.

    This decoupling between the application service and the infrastructure (
    through the generation of a CQRS-style Command) allows the service to scale
    in real-world conditions.
    """

    def __init__(self, repository: CloudProviderReadModelRepository):
        self.repository = repository

    def claim_provision(
            self,
            cluster_name: str,
            account_id: str,
            claim: ResourceClaim,
            resource_allocation: ResourceAllocation,
            cluster_endpoint: str,
            cluster_version: str = '1.9.4'
    ) -> NoReturn:
        """
        Given a resource claim for a specific provider in a specific region,
        attempts to satisfy it by generating a provisioning order (the
        Command) or raises an exception if it cannot be satisfied.

        :param cluster_name: Name of the cluster to be provisioned.
        :param account_id: Account identifier for the request.
        :param claim: ResourceClaim detailing the required resources.
        :param resource_allocation: ResourceAllocation resulting from the claim.
        :param cluster_endpoint: Endpoint for accessing the cluster.
        :param cluster_version: Version of the cluster software. Default is
            '1.9.4'.
        :return: None
        """

        # Not Implemented: Once the claim provision is created and the command
        # is sent to the command_bus. Eventually the deployment will happen and
        # the resources claimed will be used.
        # At that time, it would be nice to update the ResourceMap 'allocable'
        # resources in order to update the new total amount of resources
        # available.

        # Not Implemented but modeled: In order to have different templating
        # for different setups of the Qdrant cluster we can reuse different
        # ClusterConfigurations based on the type of costumer (free or enterprise)
        # etc.

        cluster_id = resource_allocation.compute_cluster.id

        db_cluster_configuration = DBClusterConfiguration(
            id=str(uuid.uuid5(uuid.NAMESPACE_DNS, 'dummy_template')),
            created_at=datetime.utcnow(),
            cluster_id=cluster_id,
            cluster_endpoint=cluster_endpoint,
            num_nodes=claim.num_nodes,
            node_configuration=DBNodeSpecs(
                disk=claim.disk,
                memory=claim.memory,
                cpu=claim.cpu,
            )
        )

        # For this prototype without persistence we fake the command_id
        # based on the cloud_provider_name, generating always the same message
        # even if the parameters change.
        #
        # We take this liberty to simplify the implementation and thus avoid the
        # need for a persistence layer or real messaging that could complicate
        # both the test and the statement
        command_id = str(uuid.uuid5(
            uuid.NAMESPACE_DNS, resource_allocation.cloud_provider.name))

        command = ProvisionDBCluster(
            id=command_id,
            account_id=account_id,
            cluster_id=cluster_id,
            cluster_name=cluster_name,  # Assuming no Collisions.
            cloud_provider=resource_allocation.cloud_provider.name,
            cloud_region=resource_allocation.compute_cluster.region,
            cluster_version=cluster_version,
            db_configuration=db_cluster_configuration
        )

        # Not Implemented: Persist de Allocation in order to avoid duplicates
        # in allocation claims.

        command_bus = CommandBus()
        command_bus.dispatch({command})

        app_logger.debug(f"{self.__class__.__name__}: Dispatched "
                         f"ProvisionDBCluster with payload: "
                         f"{command.as_dict()}")

        return command

    def allocate_resources(
            self,
            claim: ResourceClaim
    ) -> ResourceAllocation:
        """
        Calls the aggregate root responsible for resource allocation, based
        on the current resource map available by CloudProvider and Region.

        :param claim: ResourceClaim detailing the required resources.
        :return: A ResourceAllocation if the claim can be satisfied.
        """

        # Not implemented: When an allocation of resources is created those
        # resources are not virtually available for a new allocations. However,
        # the allocation of resource is a TENTATIVE action rather than an
        # executed action and can eventually be processed.
        # One way to approach that is using Redis or other Distributed memory
        # caching system that allow the component responsible for the allocation
        # (In our prototype the ResourceMap) consider in the free resources
        # available all the in-flight allocations.
        resource_map = self.repository.get_resource_map(claim.cloud_provider)
        return resource_map.allocate_destination_cluster_by_resources(claim)