from nexus.core.infrastructure.model.implementations import Entity


class DBCluster(Entity):
    """
    Entity that models a Qdrant DB Cluster provisioned in a Kubernetes cluster
    for an existing CloudProvider.
    """

    account_id:                       str
    db_cluster_id:                    str
    db_cluster_api_key:               str
    db_cluster_endpoint:              str
    cloud_provider:                   str
    cloud_provider_region:            str
    cloud_provider_service_endpoint:  str
