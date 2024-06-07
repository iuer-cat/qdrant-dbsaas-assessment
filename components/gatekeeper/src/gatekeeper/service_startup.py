import inspect, os
from gatekeeper.application.settings import app_logger
from gatekeeper.infrastructure.repositories.memory import \
 InMemoryRoutingRepository
from gatekeeper.infrastructure.reverse_proxy.twisted import TwistedReverseProxy
from nexus.core.application.logging import LoggingBootstrap
from nexus.core.infrastructure.repositories.db_cluster import \
 YamlDBClusterRepository

"""
What is GateKeeper?

GateKeeper is a reverse proxy service designed to sit in front of Qdrant clusters.
Assuming that Qdrant clusters secure their data using a known secret called an
api-key, which operates at the cluster level.

This service provides a common gateway or entry point for connections to Qdrant
clusters, similar to what an Ingress or an API-Gateway would do. It uniquely
validates api-keys generated through salt hashing, derived from the original
cluster's api-key.

Once it confirms that the key is derived from the original api-key, GateKeeper
replaces the HTTP Header 'api-key' with the value expected by the Qdrant cluster
and routes the connection to the default port, 6333.

The reasons and motivations for this architectural choice are detailed in
the documentation accompanying this prototype.
"""

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(
        inspect.getfile(inspect.currentframe())))
    logging_file = os.path.join(
        f'{current_path}/../../../', 'logging.yaml')
    LoggingBootstrap.configure(logging_file)

    app_logger.info(f"Bootstrap: Initializing GateKeeper service")
    # Repository that use the 'persistence_layer'
    db_cluster_repository = YamlDBClusterRepository()
    app_logger.debug(f"Bootstrap: DBClusterRepository "
                    f"<{db_cluster_repository.__class__.__name__}>")

    # Eventually this 'in-memory' might fit into Redis or other distributed
    # key-value storages.
    routing_respository = InMemoryRoutingRepository(
        db_cluster_repository=db_cluster_repository)

    app_logger.debug(f"Bootstrap: RoutingRepository "
                    f"<{routing_respository.__class__.__name__}>")

    reverse_proxy = TwistedReverseProxy(routing_repository=routing_respository)
    app_logger.info(f"Bootstrap: Starting TwistedReverseProxy at port 8081")
    reverse_proxy.run(8081)






