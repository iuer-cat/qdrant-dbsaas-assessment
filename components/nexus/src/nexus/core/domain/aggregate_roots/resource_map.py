import uuid
from typing import List

from nexus.core.domain.entities.cloud_provider import CloudProvider
from nexus.core.domain.value_objects.compute_resources import \
    ComputeCluster
from nexus.core.infrastructure.model.implementations import Entity
from orion.domain.entities.resource_allocation import ResourceAllocation
from orion.domain.exceptions import ResourceAllocationException, \
    CloudProviderRegionUnavailable
from orion.domain.value_objects.resource_claim import ResourceClaim


class CloudProviderResourceMap(Entity):
    """
    Aggregate Root responsible for finding space for provisioning a Qdrant
    cluster based on the required resources (ResourceClaim) as well as all
    existing clusters for a given CloudProvider.
    """

    id:                 str
    cloud_provider:     CloudProvider
    clusters:           List[ComputeCluster]

    def allocate_destination_cluster_by_resources(
            self,
            claim: ResourceClaim,
    ) -> ResourceAllocation:
        """
        Provisions the cluster according to the resource specifications required
        within the ResourceClaim if possible. If not possible, an exception is
        raised indicating the problem.

        :param claim: The ResourceClaim detailing the required resources.
        :return: A ResourceAllocation instance if allocation is successful.
        :raises ResourceAllocationException: If the resources cannot be allocated.
        :raises CloudProviderRegionUnavailable: If the specified cloud region
            is not available.
        """

        compute_cluster = None
        if claim.cloud_provider != self.cloud_provider.name:
            raise ResourceAllocationException(
                f'CloudProviderResourceMap[{self.cloud_provider.name}]: '
                f'Unable to allocate resources for cloud provider: '
                f'{claim.cloud_provider}')

        if claim.cloud_region not in self.cloud_provider.available_regions:
            raise CloudProviderRegionUnavailable(f'Region {claim.cloud_region} '
                                                 f'not available')

        for candidate in self.clusters:
            # Not implemented: We are not validating the total available
            # resources in the cluster, we assume optimistically the cluster
            # will be able to provision a serverless k8s workload.
            if candidate.region == claim.cloud_region:
                compute_cluster = candidate

            # Not implemented: We are not considering the cluster congestion
            # such as number of deployments, peak pressure, or other
            # infrastructure conditions that can modify the candidate election.

        if not compute_cluster:
            raise ResourceAllocationException('Unable to allocate cluster for'
                                              'the given claim workload.')

        return ResourceAllocation(
            id=str(uuid.uuid4()),  # New UUID for each new allocation
            cloud_provider=self.cloud_provider,
            compute_cluster=compute_cluster
        )