from datetime import datetime

from nexus.core.infrastructure.model.implementations import SerializableModel


class DBNodeSpecs(SerializableModel):
    """
    Serializable model that accompanies DBClusterConfiguration and determines
    the number of resources in absolute numerical format for each node of a
    Qdrant Cluster.
    """

    disk: int
    memory: int
    cpu: int


class DBClusterConfiguration(SerializableModel):
    """
    Serializable model that composes the ProvisionDBCluster command. This model
    contains all relevant information about the morphology of the cluster to be
    provisioned.
    """

    id: str
    created_at: datetime
    num_nodes: int
    cluster_id: str
    cluster_endpoint: str
    node_configuration: DBNodeSpecs