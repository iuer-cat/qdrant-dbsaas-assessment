from nexus.command_bus.domain.commands.v1.db_clusters.models import \
    DBClusterConfiguration
from nexus.core.domain.command import Command


class ProvisionDBCluster(Command):
    """

    """

    name:                       str = 'ProvisionDBCluster'
    # Arbitrary, not implemented schema validation in this POC, but an integer
    # identification is good idea when we are serializing messages, and we don't
    # want to include the schema in the message, instead of that we can retrieve
    # from a schema library.
    schema_id:                  int = 701

    cluster_id:                 str
    cluster_name:               str
    cloud_provider:             str
    cloud_region:               str
    account_id:                 str
    cluster_version:            str

    db_configuration:           DBClusterConfiguration

