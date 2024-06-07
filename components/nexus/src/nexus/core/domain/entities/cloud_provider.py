from typing import List

from nexus.core.infrastructure.model.implementations import Entity


class CloudProvider(Entity):
    """
    Entity that models a CloudProvider which has provisioned Kubernetes clusters
    for deploying Qdrant DB Clusters.
    """

    id: str
    name: str
    account_id: str
    available_regions: List[str]



