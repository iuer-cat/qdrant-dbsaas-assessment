from pydantic import BaseModel, Field


class CreateClusterConfigurationNodeConfigurationEntry(BaseModel):
    """
    Pydantic model for creating a cluster configuration node configuration
    entry.
    """

    class Config:
        extra = "forbid"

    disk: int = Field(description="Total disk size in absolute numerical "
                                  "integer, expressed internally as GB")
    memory: int = Field(description="Total memory size in absolute numerical "
                                    "integer, expressed internally as GB")
    cpu: int = Field(description="Total CPU size in absolute numerical integer, "
                                 "expressed in centennials of CPU, 1cpu is 100")


class CreateClusterConfigurationEntry(BaseModel):
    """
    Pydantic model for creating a cluster configuration entry.
    """

    class Config:
        extra = "forbid"

    # Not Implemented: Validate that the number of nodes are odd in progressions
    # as 1,3,5,7,9... in order to avoid split-brain conditions. Also limit to 19
    # as maximum number just like Qdrant Cloud does.

    num_nodes: int = Field(description="Number of nodes for the "
                                       "Qdrant DB cluster", default=1)
    node_configuration: CreateClusterConfigurationNodeConfigurationEntry = Field(
        description="Compute specifications for node resources")


class CreateClusterBodyRequest(BaseModel):
    """
    Pydantic model for creating a cluster body expected in the provision of a
    new Qdrant DB cluster.
    """

    class Config:
        extra = "forbid"

    name: str = Field(description="Unique Cluster name")
    cloud_provider: str = Field(description="Cloud provider identifier")
    cloud_region: str = Field(description="Cloud region preferred")
    configuration: CreateClusterConfigurationEntry = Field(
        description="Configuration Specification for number of nodes and node "
                    "resources")