from nexus.core.domain.entities.cloud_provider import CloudProvider
from nexus.core.domain.value_objects.compute_resources import \
    ComputeCluster
from nexus.core.infrastructure.model.implementations import Entity


class ResourceAllocation(Entity):
    """
    Entity representing a resource allocation. A factual model that can suffer
    from eventual consistency, because this is a non-materialized Qdrant DB
    Cluster provision that has been reserved but its provisioning is on-going
    (Nebula is responsible for the provision).
    """

    id:                 str
    cloud_provider:     CloudProvider
    compute_cluster:    ComputeCluster