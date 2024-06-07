from kubernetes import client, config

from nebula.application.services.kube_config import KubeConfigDiscovery
from nebula.application.settings import app_logger


class K8sNetworkingDiscoveryService:
    """
    For the GateKeeper component to route requests to Qdrant clusters, this
    domain service is responsible for identifying the K8s Load Balancer service
    in front of the Qdrant cluster and capturing its IP.
    """

    def __init__(self, cluster_id: str):
        kube_config_path = KubeConfigDiscovery.get_kube_config_path(cluster_id)
        config.load_kube_config(config_file=kube_config_path)
        self.k8s_client = client.CoreV1Api()

    def get_service_cluster_ip(self, db_cluster_id) -> str:
        """
        Based on the service name, which is discoverable via naming
        convention, retrieve the IP of the Kubernetes LoadBalancer.

        :param db_cluster_id: The unique identifier for the DB Cluster.
        :return: The cluster IP of the LoadBalancer service.
        """

        service_name = f"qdrant-{db_cluster_id}"
        namespace = "default"

        service = self.k8s_client.read_namespaced_service(
            name=service_name,
            namespace=namespace
        )
        cluster_ip = service.spec.cluster_ip

        app_logger.debug(f"{self.__class__.__name__}: Discovered Cluster IP: "
                         f"{cluster_ip}, for DBCluster: {db_cluster_id}")

        return cluster_ip

