import inspect, os, yaml, glob
from typing import NoReturn, List

from nexus.core.domain.entities.db_cluster import DBCluster
from nexus.core.domain.ports import DBClusterWriteModelRepository, \
    DBClusterReadModelRepository


class YamlDBClusterRepository(
    DBClusterWriteModelRepository,
    DBClusterReadModelRepository
):
    """
    Implementation of a DBCluster repository for both ReadModel and WriteModel
    for the DBCluster entity.

    This implementation uses the 'persistence_layer' and has been created solely
    for prototype and demonstration purposes.
    """

    def save(
            self,
            db_cluster: DBCluster,
    ) -> NoReturn:
        """
        Persists a db_cluster entity in the repository.

        :param db_cluster: The DBCluster entity to be persisted.
        """
        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

        db_cluster_file_path = os.path.join(
            f'{current_path}/../../../../../../../'
            f'persistence_layer/db_clusters/',
            f"{db_cluster.db_cluster_id}.yaml")

        with open(db_cluster_file_path, "w") as yml_file:
            yaml.dump(db_cluster.as_dict(), yml_file, default_flow_style=False)

    def get_by_id(
            self,
            db_cluster_id: str,

    ) -> DBCluster:
        """
        Retrieve a DBCluster entity by its unique identifier.

        :param db_cluster_id: The unique identifier of the DBCluster.
        :return: The DBCluster entity with the given id.
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

        db_cluster_file_path = os.path.join(
            f'{current_path}/../../../../../../../'
            f'persistence_layer/db_clusters/',
            f"{db_cluster_id}.yaml")

        with open(db_cluster_file_path, "r") as yml_file:
            dc_cluster_dict = yaml.safe_load(yml_file)
            return DBCluster(**dc_cluster_dict)

    def get_all(self) -> List[DBCluster]:
        """
        Retrieve all DBCluster entities that exist in the repository.

        :return: List of DBCluster entities.
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        db_clusters_path = os.path.join(
            f'{current_path}',
            '../../../../../../../persistence_layer/db_clusters/')

        db_clusters = list()
        pattern = f"{db_clusters_path}*.yaml"

        for file_path in glob.iglob(pattern, recursive=False):
            with open(file_path, "r") as yml_file:
                dc_cluster_dict = yaml.safe_load(yml_file)
                db_clusters.append(DBCluster(**dc_cluster_dict))

        return db_clusters
