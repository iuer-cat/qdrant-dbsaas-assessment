from gatekeeper.application.settings import app_logger
from gatekeeper.domain.ports import RoutingRepository
from gatekeeper.domain.services.api_key import ApiKeyEnforcingService
from gatekeeper.domain.value_objects.request import Route, ProxyRequest


class RoutingService:
    """
    RoutingService is responsible for intercepting and handling incoming requests
    to ensure they are authenticated and correctly redirected to the appropriate
    Qdrant clusters.
    """

    def __init__(self,  routing_repository: RoutingRepository):
        self.routing_repository = routing_repository

    def intercept_request(self, request: ProxyRequest) -> ProxyRequest:
        """
        Processes a request to validate the API key using the designated
        application service and identifies the 'internal' endpoint within the
        proposed infrastructure suitable for routing requests to the
        corresponding Qdrant cluster.

        If the API key is valid, the method sets up the proxy destination by
        filling in the internal endpoint of the Qdrant cluster and the
        standard port 6333. It also includes the internal API key of the
        Qdrant cluster, which is the only key recognized by the cluster
        (either an API key or a JWT signed by the API key).

        :param request: ValueObject representing the request containing the API
            key and the original host.
        :return: Modified ValueObject with the appropriate proxy route if the
            validation is successful.
        """

        db_cluster = self.routing_repository.get_by_endpoint(
            request.original.host)

        # Endpoint not recognized
        if not db_cluster:
            app_logger.debug(f"{self.__class__.__name__}: Endpoint "
                             f"{request.original.host}, Not Found! Routing is "
                             f"not possible.")
            return request

        secret = db_cluster.db_cluster_api_key
        request.authenticated = ApiKeyEnforcingService.is_valid_api_key(
            api_key=request.original.api_key, secret=secret
        )

        app_logger.debug(f"{self.__class__.__name__}: Authenticated Request to "
                         f"{request.original.host}, using api-key: "
                         f"{request.original.api_key[:5]}")

        request.proxy_to = Route(
            host=db_cluster.db_cluster_endpoint,
            port=6333,  # Hardcoded By now to reduce complexity
            api_key=db_cluster.db_cluster_api_key
        )

        app_logger.debug(f"{self.__class__.__name__}: Generating Proxy Route to "
                         f"{db_cluster.db_cluster_endpoint}:6333, Qdrant "
                         f"api-key: {db_cluster.db_cluster_api_key[:5]}")

        return request