from abc import abstractmethod, ABC
from typing import NoReturn, List

from nexus.core.domain.entities.db_cluster import DBCluster


class DBClusterRepository(ABC):
    """
    DDD Port and base class for the different repositories for DBCluster models.
    """
    pass


class DBClusterWriteModelRepository(DBClusterRepository):
    """
    DDD Port for the DBCluster write repository. The segregation of ReadModel
    and WriteModel is not implemented, but these interfaces or ports could model
    this behavior.

    This could be a good point of discussion to debate the CAP theorem and the
    trade-offs of denormalization.
    """

    @abstractmethod
    def save(
            self,
            db_cluster: DBCluster,

    ) -> NoReturn:
        """
        Persists a db_cluster entity in the repository.

        :param db_cluster: The DBCluster entity to be persisted.
        """
        raise NotImplementedError()


class DBClusterReadModelRepository(DBClusterRepository):
    """
    DDD Port for the DBCluster write repository. The segregation of ReadModel
    and WriteModel is not implemented, but these interfaces or ports could model
    this behavior.

    This could be a good point of discussion to debate the CAP theorem and the
    trade-offs of denormalization.
    """

    @abstractmethod
    def get_all(self) -> List[DBCluster]:
        """
        Retrieve all DBCluster entities that exist in the repository.

        :return: List of DBCluster entities.
        """

        raise NotImplementedError()

    @abstractmethod
    def get_by_id(
            self,
            db_cluster_id: str,

    ) -> DBCluster:
        """
        Retrieve a DBCluster entity by its unique identifier.

        :param db_cluster_id: The unique identifier of the DBCluster.
        :return: The DBCluster entity with the given id.
        """

        raise NotImplementedError()