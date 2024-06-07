import uuid
from typing import Optional


class DBClusterEndpointService:
    """
    This service is responsible for generating endpoints, based on the assumption
    that by default all provisioned Qdrant DB Clusters will not be exposed to
    the internet and will be private, either via a VPC, peering, an endpoint,
    or through a firewall or security group that controls access.

    Based on this assumption, the GateKeeper component becomes the only access
    point to the Qdrant DB Clusters, with a multi-tenant approach.

    Therefore, to uniquely identify one cluster from another, the concept of an
    endpoint will be generated. This is essentially a unique DNS record specific
    to accessing that cluster through the GateKeeper reverse-proxy component,
    without exposing the internal API key provided by the Qdrant application.

    NOTE: This implementation is conceptual, as once the endpoint is generated,
    the required DNS records and associated SSL certificates (via
    AlternativeSubjName) are not being created, which might be mandatory for a
    real implementation.
    """

    # For prototyping purposes we are assuming localhost as TLD
    DEFAULT_ZONE_ID: str = 'localhost'

    def __init__(
            self,
            cluster_name: str,
            account_id: str,
            cloud_region: str,
            cloud_provider: str,
            zone_id: Optional[str] = None,
    ):
        self.cluster_name = cluster_name
        self.account_id = account_id
        self.cloud_region = cloud_region
        self.cloud_provider = cloud_provider

        if not zone_id:
            self.zone_id = self.DEFAULT_ZONE_ID
        else:
            self.zone_id = zone_id

    def register(self) -> str:
        """
        Composes the subdomain and eventually may call the Domain Services
        responsible for SSL generation and DNS record creation if needed.

        :return: Fully qualified domain name for the cluster endpoint.
        """

        subdomain = self.__create_endpoint_name()
        # Not Implemented: Register the new A/CNAME Record to the SOA zone

        return f'{subdomain}.{self.cloud_region}.{self.cloud_provider}.{self.zone_id}'

    def __create_endpoint_name(self) -> str:
        """
        Generates a predictable UUID based on the cluster_name and
        account_id that identifies the tenant owner of the cluster.

        :return: A unique subdomain name as a string.
        """

        return str(
            uuid.uuid5(
                namespace=uuid.NAMESPACE_DNS,
                name=f'{self.cluster_name}-{self.account_id}'
            )
        )