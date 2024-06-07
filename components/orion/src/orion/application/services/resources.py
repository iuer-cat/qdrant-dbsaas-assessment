import inspect, os, yaml

from nexus.core.domain.aggregate_roots.resource_map import \
    CloudProviderResourceMap


class ResourceLoaderService:
    """
    This service assumes that Draftsman has generated resource maps with the
    total resources of the cluster and has persisted them within the
    'persistence_layer' directory named 'resource_maps'.

    Similar to the other data in the 'persistence_layer', this is an assumption
    made to simplify and streamline the prototype's implementation.
    """

    def load_from_file(self, file_name) -> CloudProviderResourceMap:
        """
        Loads the file associated with the given cloud provider name.

        :param file_name: The name of the file to load.
        :type file_name: str
        :return: A CloudProviderResourceMap instance initialized with
                 the data from the file.
        :rtype: CloudProviderResourceMap
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))

        config_file_path = os.path.join(
            f'{current_path}/../../../../../../persistence_layer/resource_maps/', file_name)

        with open(config_file_path, "r") as yml_file:
            resource_map_dict = yaml.safe_load(yml_file)
            return CloudProviderResourceMap(**resource_map_dict)