from abc import abstractmethod, ABC
from typing import NoReturn

from nebula.domain.entities.db_cluster_specs import DBClusterSpecs
from nexus.core.domain.message import Message


class Handler(ABC):
    """
    DDD Port that unifies handlers. Handlers are message processors,
    and the Bus should have handlers associated with the messages
    it receives.
    """

    @abstractmethod
    def handle(
            self,
            message: Message
    ) -> NoReturn:
        """
        Method called for each message received by the bus.

        :param message: The message to be processed by the handler.
        """

        raise NotImplementedError()


class InfrastructureClient(ABC):
    """
    DDD Port that unifies the provisioning method for infrastructure in a
    Kubernetes cluster. In this prototype, the implementation is based on Helm
    Chart, as Qdrant provides a Helm Chart for cluster installation.

    However, other implementations based on Kubernetes primitives (PVC, Stateful
    Sets, ...) and the Kubernetes client library, or via CRD and an operator,
    could be valid implementations that could work out-of-the-box if they follow
    this interface.
    """

    @abstractmethod
    def provision(
            self,
            cluster_id: str,
            specs: DBClusterSpecs
    ) -> NoReturn:
        """
        Provision the infrastructure for a given Qdrant DB Cluster
        using the specified cluster ID and specifications.

        :param cluster_id: The unique identifier for the cluster.
        :param specs: The specifications for the DB Cluster.
        """

        raise NotImplementedError()