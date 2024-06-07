from enum import Enum

from nexus.core.domain.aggregate_roots.resource_map import \
    CloudProviderResourceMap

from orion.application.services.resources import ResourceLoaderService
from orion.domain.exceptions import CloudProviderNotFound
from orion.domain.ports import CloudProviderReadModelRepository


class Files(Enum):
    LOCAL: str = "local.yaml"
    AWS_TEST: str = "aws.yaml"


class YamlCloudProviderRepository(
    CloudProviderReadModelRepository
):
    """
    Implementation of the repository for entities of type
    CloudProviderResourceMap using the 'persistence_layer'
    """

    def __init__(self) -> None:
        self.loader_service = ResourceLoaderService()

    def get_resource_map(
            self,
            cloud_provider: str,
    ) -> CloudProviderResourceMap:
        """
        Based on the provider's name (e.g., 'aws-account_id'),
        retrieves the existing resource map.

        :param cloud_provider: The name of the cloud provider.
        :type cloud_provider: str
        :return: The resource map of the specified CloudProvider.
        :rtype: CloudProviderResourceMap
        """

        if cloud_provider == 'minikube':
            return self.loader_service.load_from_file(Files.LOCAL.value)
        if cloud_provider == 'aws':
            return self.loader_service.load_from_file(Files.AWS_TEST.value)

        raise CloudProviderNotFound(f"Invalid cloud provider: {cloud_provider}")