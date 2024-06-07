import json
from twisted.internet import reactor
from twisted.web import proxy, server, resource, http
from typing import NoReturn, Callable

from gatekeeper.application.services.routing import RoutingService
from gatekeeper.application.settings import app_logger
from gatekeeper.domain.ports import ReverseProxy, RoutingRepository
from gatekeeper.domain.value_objects.request import ProxyRequest, Route


class UnAuthorizedResource(resource.Resource):
    """
    Custom UnAuthorizedResource implementation for the prototype purpose.
    """

    # Indicates the end of the process and ensure the render will be sent
    # immediately to the client
    isLeaf = True

    def render(self, request):
        """
        Twisted style Response with a 401 Unauthorized status and a JSON body
        indicating an error due to unauthorized access.

        :param request: The incoming HTTP request.
        :return: bytes - The JSON encoded error message.
        """

        request.setHeader('Content-Type', 'application/json')
        request.setResponseCode(http.UNAUTHORIZED)
        error_message = json.dumps(
            {"error": "Unauthorized", "status": 401})
        return error_message.encode('utf-8')


class NotFoundResource(resource.Resource):
    """
    Custom NotFoundResource implementation for the prototype purpose.
    This NotFound is raised for unknown Qdrant cluster endpoints.
    """

    # Indicates the end of the process and ensure the render will be sent
    # immediately to the client
    isLeaf = True

    def render(self, request):
        """
        Twisted style Response with a 404 Not Found status and a JSON body
        indicating that the requested DBCluster endpoint is not found.

        :param request: The incoming HTTP request.
        :return: bytes - The JSON encoded error message.
        """

        request.setHeader('Content-Type', 'application/json')
        request.setResponseCode(http.NOT_FOUND)
        error_message = json.dumps(
            {"error": "DBCluster Endpoint Not Found", "status": 404})
        return error_message.encode('utf-8')


class CustomReverseProxyResource(proxy.ReverseProxyResource):
    """
    A custom reverse proxy resource that intercepts requests, applies
    authentication and routing logic, and forwards them to the appropriate
    Qdrant cluster endpoint.
    """

    def __init__(
            self,
            host='',
            port=0,
            path='',
            reactor=reactor,
            request_interceptor: Callable = None):
        super().__init__(host, port, path, reactor=reactor)
        self.request_interceptor = request_interceptor

    def getChild(self, path, request):
        """
        Called when a child resource (Twisted internal stuff) is requested,
        allowing the proxy to handle dynamic routing based on the original
        request headers and URI.

        :param path: str - The requested path.
        :param request: The incoming HTTP request.
        :return: Resource - The appropriate web resource based on authentication
            and routing logic.
        """
        host = request.getHeader('host').split(':')[0]
        api_key = request.getHeader('api-key')

        if api_key:
            app_logger.debug(f"Twisted - Received request: "
                             f"{request.uri.decode('ascii')}, endpoint: "
                             f"{host}, and api-key: {api_key[:5]}")

        if not api_key:
            app_logger.debug(f"Twisted - No api-key provided, Unautorized!")
            return UnAuthorizedResource()

        proxy_request = ProxyRequest(
            original=Route(
                host=host, api_key=api_key,
                port=0  # The original port is Negligible for this use case.
            )
        )
        path = request.path

        proxy_request = self.request_interceptor(proxy_request)

        if not proxy_request.proxy_to:
            app_logger.debug(f"Twisted - Unable to proxy pass request, "
                             f"unrecognized endpoint: {host}")
            return NotFoundResource()

        if not proxy_request.authenticated:
            app_logger.info(f"Twisted - Authentication failed! provide api-key: "
                            f"{api_key} is invalid")
            return UnAuthorizedResource()

        request.requestHeaders.setRawHeaders(
            "api-key", [proxy_request.proxy_to.api_key])

        app_logger.info(f"Twisted - Proxy passing request to: http://"
                        f"{proxy_request.proxy_to.host}:"
                        f"{proxy_request.proxy_to.port}"
                        f"{request.uri.decode('ascii')}")

        return CustomReverseProxyResource(
            proxy_request.proxy_to.host,
            proxy_request.proxy_to.port,
            path
        )


class TwistedReverseProxy(ReverseProxy):
    """
    Implements the ReverseProxy port using the Twisted framework to handle
    incoming HTTP requests, apply intercepting logic, and forward them to the
    Qdrant cluster endpoint with the proper api-key.
    """

    def __init__(self, routing_repository: RoutingRepository):
        self.routing_repository = routing_repository
        self.routing_service = RoutingService(self.routing_repository)

    def intercept_request(self, request: ProxyRequest) -> ProxyRequest:
        """
        Intercepts and modifies a request based on routing rules.

        :param request: Request - The original request to be intercepted.
        :return: Request - The modified request after applying routing logic.
        """

        request = self.routing_service.intercept_request(request)
        return request

    def run(
            self,
            port: int,

    ) -> NoReturn:
        """
        Starts the reverse proxy service, listening on the specified port.

        :param port: int - The port number on which the reverse proxy will
            listen.
        """
        site = server.Site(CustomReverseProxyResource(
            request_interceptor=self.intercept_request
        ))
        reactor.listenTCP(port, site)
        reactor.run()