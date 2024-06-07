import inspect, os

from nebula.application.handlers.db_cluster.provision import \
  ProvisionDBClusterHandler
from nebula.application.settings import app_logger
from nebula.infrastructure.clients.helm import HelmInfrastructureClient
from nebula.infrastructure.consumer import SingleThreadCommandBusConsumer
from nexus.command_bus.application.command_bus import CommandBus
from nexus.core.application.logging import LoggingBootstrap

from nexus.core.infrastructure.repositories.db_cluster import \
  YamlDBClusterRepository

"""
What is Nebula?

Nebula is an asynchronous service or worker responsible for processing
heavy-duty requests, such as provisioning clusters.

Essentially, this service is a separation of responsibilities from the API, 
due to the nature of infrastructure provisioning itself (the Qdrant cluster)
and the inherent aspects of K8s. In any case, provisioning can never be
synchronous and must always be eventually consistent.

This component adds complexity to the test; however, this separation of
responsibilities and the centralization of provisioning logic into a separate
component seemed more understandable within the hypothetical context of 
needing to extend provisioning to multi-provider cloud environments 
(Google, AWS, Azure...). This segregation, along with the abstractions made 
here, presupposes easy extensibility and high cohesion.
"""


if __name__ == "__main__":
  current_path = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
  logging_file = os.path.join(
    f'{current_path}/../../../', 'logging.yaml')
  LoggingBootstrap.configure(logging_file)

  app_logger.info(f"Bootstrap: Initializing Nebula service")

  # Command Bus that use the 'persistence_layer'
  bus = CommandBus()
  message_handler = ProvisionDBClusterHandler(

    # Infrastructure Client based on Helm instead of k8s Operator
    infrastructure_client=HelmInfrastructureClient(),

    # Repository that use the 'persistence_layer'
    db_cluster_repository=YamlDBClusterRepository()
  )

  # Single Thread and one-by-one Command Consumer.
  command_consumer = SingleThreadCommandBusConsumer(
    bus=bus,
    message_handler=message_handler,
  )

  command_consumer.run()


