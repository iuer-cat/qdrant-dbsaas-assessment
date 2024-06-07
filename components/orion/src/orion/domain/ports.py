from abc import abstractmethod, ABC

from nexus.core.domain.aggregate_roots.resource_map import \
    CloudProviderResourceMap


class CloudProviderReadModelRepository(ABC):
    """
    DDD Port that serves as a contract for repository implementations
    containing the resource map for a given CloudProvider.
    """

    @abstractmethod
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

        raise NotImplementedError()