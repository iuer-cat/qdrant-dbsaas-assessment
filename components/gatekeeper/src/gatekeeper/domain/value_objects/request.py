from typing import Dict, Optional

from nexus.core.infrastructure.model.implementations import ValueObject


class Route(ValueObject):
    """
    ValueObject that represents the connection information to a Qdrant cluster.
    This object includes the public access endpoint (host), an optional port,
    and the necessary api-key for authentication. The api-key is also validated
    by GateKeeper using salt hashing techniques before being sent to the Qdrant
    cluster, which validates the specified api-key during deployment.
    """

    host: str
    port: int
    api_key: str


class ProxyRequest(ValueObject):
    """
    ValueObject representing a high-level request used in the RoutingService.
    It essentially encapsulates the original routing that carries the request
    and includes fields for the proxied route to which the request will be sent
    if the RoutingService during its interception has specific entries for a
    given host and the api-key is verified.
    """

    original: Route
    proxy_to: Optional[Route] = None
    authenticated: bool = False
    additional_headers: Dict[str, str] = {}