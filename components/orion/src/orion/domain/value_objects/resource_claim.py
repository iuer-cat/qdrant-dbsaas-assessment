from nexus.core.infrastructure.model.implementations import ValueObject


class ResourceClaim(ValueObject):
    """
    Value object representing the total amount of resources claimed by a
    requester, for the provisioning of a new Qdrant DB Cluster.

    """

    cloud_provider: str
    cloud_region:   str
    num_nodes:      int
    disk:           int
    memory:         int
    cpu:            int