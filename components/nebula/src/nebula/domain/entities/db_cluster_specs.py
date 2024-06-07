from nexus.core.infrastructure.model.implementations import Entity


class DBClusterSpecs(Entity):
    """
    Simplified model of the specifications for a Qdrant DB Cluster with the
    minimum configurable parameters required in the technical test.
    """

    id:         str
    name:       str
    api_key:    str
    num_nodes:  int
    disk:       int
    memory:     int
    cpu:        int
