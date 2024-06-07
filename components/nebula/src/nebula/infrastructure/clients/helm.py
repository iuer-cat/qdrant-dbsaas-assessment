import inspect, os, yaml
from jinja2 import Environment, FileSystemLoader
from typing import NoReturn, Dict
from avionix import ChartBuilder, ChartDependency, ChartInfo

from nebula.application.services.kube_config import KubeConfigDiscovery
from nebula.application.settings import app_logger
from nebula.domain.entities.db_cluster_specs import DBClusterSpecs
from nebula.domain.ports import InfrastructureClient


class HelmInfrastructureClient(InfrastructureClient):
    """
    Implementation of the infrastructure client using Helm and the official
    Qdrant Chart.

    Helm was chosen because the Helm Chart is the only easily accessible
    resource available. I would have liked to try the Kubernetes Operator.
    """

    def __get_qdrant_chart_path(self) -> str:
        """
        Due to limitations of the avionix library, we have downloaded a local
        copy of the Qdrant Chart.

        :return: The file path to the local Qdrant Helm Chart.
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        qdrant_chart_path = os.path.join(
            f'{current_path}', '../../../../../../charts/qdrant')
        return qdrant_chart_path

    def _render_helm_chart_values(self, specs: DBClusterSpecs) -> Dict:
        """
        Generates a values.yaml file suitable for use in the Helm Chart, with
        specifications such as the number of nodes, the api_key, and the
        computational resources per node in absolute numerical values.

        :param specs: The DBClusterSpecs object containing the
                      specifications.
        :return: A dictionary representation of the Helm values.yaml.
        """

        current_path = os.path.dirname(os.path.abspath(
            inspect.getfile(inspect.currentframe())))
        qdrant_chart_values_template_path = os.path.join(
            f'{current_path}', f'../templates/')

        file_loader = FileSystemLoader(qdrant_chart_values_template_path)
        env = Environment(loader=file_loader)
        template = env.get_template('qdrant_values.j2')

        data = {
            'num_nodes': specs.num_nodes,
            'api_key': specs.api_key,
            'disk_gi': f'{specs.disk}Gi',
            'memory_mi': f'{specs.memory}Mi',
            'cpu_units': f'{specs.cpu}m',
        }

        values_yaml_str = template.render(data)

        values_dict = yaml.safe_load(values_yaml_str)

        app_logger.debug(f"{self.__class__.__name__}: Generated Helm Chart "
                         f"values.yaml with content: {values_dict}")

        return values_dict

    def _get_chart_builder(self, specs: DBClusterSpecs) -> ChartBuilder:
        """
        Due to limitations of the avionix library, we need to generate a local
        chart where the Qdrant Chart is a dependency, essentially creating a
        type of Meta-Chart.

        :param specs: The DBClusterSpecs object containing the
                      specifications.
        :return: A ChartBuilder object for building and installing
                 the Helm Chart.
        """
        qdrant_chart_path = self.__get_qdrant_chart_path()

        return ChartBuilder(
            ChartInfo(
                api_version="3.2.4",
                name=f"qdrant-{specs.id}",
                version="0.1.0",
                app_version="v1",
                dependencies=[
                    ChartDependency(
                        "qdrant",
                        "0.9.0",
                        f"file://{qdrant_chart_path}",
                        "local-repo",
                        is_local=True,
                        values=self._render_helm_chart_values(specs=specs),
                    ),
                ],
            ),
            [],
        )

    def provision(
            self,
            cluster_id: str,
            specs: DBClusterSpecs
    ) -> NoReturn:
        """
        Using the specific kube_config file for the target cluster, installs
        the Helm Chart.

        :param cluster_id: The unique identifier for the cluster.
        :param specs: The DBClusterSpecs object containing the
                      specifications.
        """

        kube_config_path = KubeConfigDiscovery.get_kube_config_path(cluster_id)
        chart_builder = self._get_chart_builder(specs)
        chart_builder.install_chart(
            {
                "dependency-update": None,
                "kubeconfig": kube_config_path,
            }
        )
        app_logger.debug(f"{self.__class__.__name__}: Qdrant Chart installed on "
                         f"cluster {cluster_id}, using kube_config "
                         f"{kube_config_path}")