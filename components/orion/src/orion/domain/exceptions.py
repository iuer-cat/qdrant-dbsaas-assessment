
class CloudProviderNotFound(Exception):
    """Raised when cloud provider is not found."""
    pass


class CloudProviderRegionUnavailable(Exception):
    """Raised when cloud provider region is not available."""
    pass


class ResourceAllocationException(Exception):
    """
    Never Raised But Modeled, When the Allocation fails for CloudProvider
    or K8s Cluster Limits
    """
    pass