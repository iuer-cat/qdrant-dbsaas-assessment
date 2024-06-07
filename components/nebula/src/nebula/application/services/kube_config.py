import inspect, os

from nebula.application.settings import app_logger


class KubeConfigDiscovery:
    """
    NOTE: SKETCHED RATHER THAN IMPLEMENTED !!!!!

    This application service assumes that the Draftsman component (responsible
    for provisioning the REAL infrastructure in  cloud providers) outputs files
    located under the directory 'persistence_layer/kube_configs'.

    Draftsman is expected to provision a Kubernetes cluster for a given cloud
    provider in a specific region and generate a base kube_config configuration
    (or similar information) for that Kubernetes cluster.

    When a new Qdrant DB Cluster is provisioned, it is assigned a Kubernetes
    cluster and a DB Cluster ID (cluster_id). At this point, Somehow the service
    will generates the necessary kube_config file for the infrastructure client
    to provision the cluster, based on the K8S_CLUSTER kube_config file
    generated previously by Draftsman.

    Eventually, two Qdrant DB Clusters might have different kube_config files
    that are completely identical. Despite this duplication issue, we prefer
    the flexibility of having separate kube_config files for each Qdrant
    provisioning.

    Example:

    - Qdrant DB Cluster 1:
      - Provisioned in Kubernetes cluster 'k8s-cluster-1'.
      - Draftsman generates a kube_config file for k8s-cluster-1
        and saves it in
        'persistence_layer/kube_configs/k8s-cluster-1_kube_config'.
      - Based on the Specs, Nebula will generate the specific kube_config file
      and save it in 'persistence_layer/kube_configs/cluster_id_1/config'

    - Qdrant DB Cluster 2:
      - Also provisioned in Kubernetes cluster 'k8s-cluster-1'.
      - Draftsman will not generate anything because it was generated
        previously.
      - Based on the Specs, Nebula will generate the specific kube_config file
        and save it in 'persistence_layer/kube_configs/cluster_id_2/config'

    Although both kube_config files might be identical in content,
    they are separated by cluster_id, providing greater flexibility
    in the management and provisioning of Qdrant clusters.

    NOTE: This workflow is actually performed manually for the prototype,
    in a production-ready scenario, Draftsman will store the cluster information
    including the IAM data somewhere and the kube_config files will be
    generated on-the-fly or through the kubernetes Python Client.

    This approach has created only for DEMONSTRATIVE purposes for all the pieces
    involved into the PROVISIONING Workflow
    """

    @staticmethod
    def get_kube_config_path(cluster_id: str) -> str:
        """
        Returns the path to the kube_config file for the given
        cluster_id.

        :param cluster_id: The unique identifier for the Qdrant DB Cluster.
        :return: The file path to the kube_config for the specified cluster_id.
        """
        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        kube_config_path = os.path.join(
            f'{current_path}',
            f'../../../../../../persistence_layer/kube_configs/{cluster_id}/config')

        app_logger.debug(f"{KubeConfigDiscovery.__class__.__name__}: Loading "
                         f"kube_config file from {kube_config_path}")

        return kube_config_path
