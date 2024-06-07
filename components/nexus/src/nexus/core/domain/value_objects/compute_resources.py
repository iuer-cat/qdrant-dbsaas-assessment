from nexus.core.infrastructure.model.implementations import ValueObject


class ComputeCluster(ValueObject):
    """
    The -1 in resources is a flag to indicate that the Kubernetes clusters
    is based on serverless, and for the volume of the prototype we can
    assume no limits or constraints in terms of provisioning new Resources
    such Pods or Volumes.

    Of course this is a really optimistic assumption far from the reality,
    of a production ready workload. However on the context of this prototype
    is fair enough.
    """

    id: str
    region: str
    engine: str  # EKS. Minikube, Kops, Fargate, AKS GKE
    total_disk:     int = -1
    total_memory:   int = -1
    total_cpu:      int = -1
