from typing import NoReturn, Dict, Union

from gatekeeper.domain.ports import RoutingRepository
from nexus.core.domain.entities.db_cluster import DBCluster
from nexus.core.domain.ports import DBClusterRepository


class InMemoryRoutingRepository(RoutingRepository):
    """
    An in-memory implementation of the RoutingRepository. This repository
    uses a dictionary to store and retrieve mappings from endpoints to
    DBCluster instances (see the README.md into the directory
    'persistence_layer' for more details).
    """

    routing_map: Dict[str, DBCluster]

    def __init__(self, db_cluster_repository: DBClusterRepository):
        self._db_cluster_repository = db_cluster_repository
        self.routing_map = {}
        self.__load_all_entries()

    def __load_all_entries(self) -> NoReturn:
        """
        Loads all DBCluster entries from the DBClusterRepository into the
        routing map. Loading everything in memory we avoid access disk for
        every single request.
        """
        db_clusters = self._db_cluster_repository.get_all()
        for db_cluster in db_clusters:
            endpoint = db_cluster.cloud_provider_service_endpoint
            self.routing_map[endpoint] = db_cluster

    def get_by_endpoint(
            self,
            endpoint: str,
    ) -> Union[DBCluster, None]:
        """
        Retrieves the DBCluster associated with the given endpoint from the
        in-memory routing map.

        :param endpoint: str - The endpoint for which to retrieve the DBCluster.
        :return: Union[DBCluster, None] - The DBCluster object if found,
            otherwise None.
        """

        # For prototyping and testing purposes
        # We Reload all clusters in order to discover new clusters
        # and reset removed ones.
        self.__load_all_entries()

        return self.routing_map.get(endpoint, None)