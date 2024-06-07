from typing import NoReturn

from nebula.application.settings import app_logger
from nebula.domain.entities.db_cluster_specs import DBClusterSpecs
from nebula.domain.ports import Handler, InfrastructureClient
from nebula.domain.services.api_keys import DBClusterApiKeyService
from nebula.domain.services.kubernetes import K8sNetworkingDiscoveryService
from nexus.command_bus.domain.commands.v1.db_clusters.provision import \
    ProvisionDBCluster
from nexus.core.domain.entities.db_cluster import DBCluster
from nexus.core.domain.ports import DBClusterRepository


class ProvisionDBClusterHandler(Handler):
    """
    Handles provisioning of Qdrant clusters as part of a command bus system.
    It acts upon receiving ProvisionDBCluster commands, ensuring that the
    cluster is set up according to provided specifications.

    Main responsibilities:
    - Generates an API key for the new Qdrant cluster.
    - Configures the cluster specs and requests the infrastructure client
      to provision the cluster.
    - Discovers and logs the network settings of the newly created cluster.
    """

    def __init__(
            self,
            infrastructure_client: InfrastructureClient,
            db_cluster_repository: DBClusterRepository
    ) -> NoReturn:
        self.infrastructure_client = infrastructure_client
        self.db_cluster_repository = db_cluster_repository

    def handle(
            self,
            command: ProvisionDBCluster
    ) -> NoReturn:
        """
        Processes each command one by one. Under ideal conditions, the CommandBus
        recognizes that the message has been processed correctly if there are no
        exceptions, and it proceeds to mark it as processed/confirmed in the
        message broker. (Note: Message retry in the CommandBus is not
        implemented.)
        """

        if not isinstance(command, ProvisionDBCluster):
            app_logger.error(f"{self.__class__.__name__}: Unexpected Command "
                             f"type: ProvisionDBCluster")
            return None

        cluster_id = command.cluster_id
        db_config = command.db_configuration

        app_logger.info(f"{self.__class__.__name__}: Processing Qdrant "
                         f"cluster provision, cluster_id: {cluster_id}, "
                         f"db_configuration: {db_config}")

        api_key = DBClusterApiKeyService.generate()
        app_logger.debug(f"{self.__class__.__name__}: Generated Qdrant Cluster "
                         f"api key: {api_key[:5]}, cluster_id: {cluster_id}")

        specs = DBClusterSpecs(
            name=command.cluster_name,
            id=db_config.cluster_id,
            num_nodes=db_config.num_nodes,
            disk=db_config.node_configuration.disk,
            memory=db_config.node_configuration.memory,
            cpu=db_config.node_configuration.cpu,
            api_key=api_key
        )
        self.infrastructure_client.provision(
            cluster_id=cluster_id,
            specs=specs
        )

        k8s_service = K8sNetworkingDiscoveryService(cluster_id=cluster_id)
        cluster_ip = k8s_service.get_service_cluster_ip(
            db_cluster_id=db_config.cluster_id)

        app_logger.info(
            f"{self.__class__.__name__}: Qdrant Cluster Provisioned, "
            f"cluster_id: {cluster_id}, specs: {specs}, k8s cluster_ip: "
            f"{cluster_ip}")

        db_cluster = DBCluster(
            account_id=command.account_id,
            db_cluster_id=db_config.cluster_id,
            db_cluster_api_key=api_key,
            db_cluster_endpoint=cluster_ip,
            cloud_provider=command.cloud_provider,
            cloud_provider_region=command.cloud_region,
            cloud_provider_service_endpoint=command.db_configuration.cluster_endpoint
        )

        self.db_cluster_repository.save(db_cluster)