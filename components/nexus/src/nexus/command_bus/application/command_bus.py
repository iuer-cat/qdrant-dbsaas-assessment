from typing import Optional, NoReturn, List, Set

from nexus.command_bus.domain.ports import CommandPublisher, CommandSubscriber
from nexus.command_bus.infrastructure.implementations import \
    DiskCommandPublisher, DiskCommandSubscriber
from nexus.core.domain.command import Command


class CommandBus:
    """
    A simplified version of a CommandBus. The main advantage of having a
    command_bus as the layer responsible for the publication and reception of
    messages in a distributed architecture is the ease of changing or modifying
    the behavior of the message broker for publishing or subscribing.

    Benefits:
    - Separation of Concerns: Decouples business logic from message transport
      details, making the code more modular and manageable.
    - Flexibility: Easily switch or scale the messaging system (e.g., from
      disk-based to distributed systems like RabbitMQ or Kafka) without
      affecting business logic.
    - Ease of Testing: Enables the use of dummy or mock implementations for
      unit tests, allowing business logic to be tested without the need for
      full messaging infrastructure, thus making tests faster and targeted.
    - Maintainability: Reduces coupling between components, facilitating
      updates, maintenance, and evolution of the system. Infrastructure changes
      can be made in isolation without impacting business logic.

    MAJOR REASON I IMPLEMENTED HERE: I have the code already done, so it
    speed up my work in this tech test. Do not consider this as a Feature
    consider it a leverage code/library in order to get the things done quickly.
    """

    def __init__(
        self,
        publisher: Optional[CommandPublisher] = None,
        subscriber: Optional[CommandSubscriber] = None,
    ):
        if publisher:
            self.publisher = publisher
        else:
            self.publisher = DiskCommandPublisher()
        if subscriber:
            self.subscriber = subscriber
        else:
            self.subscriber = DiskCommandSubscriber()

    def retrieve(self) -> List[Command]:
        """
        Indirection layer to receive messages from the subscriber (
        infrastructure implementation), specifically Command messages.

        :return: List of Command messages retrieved by the subscriber.
        """
        return self.subscriber.retrieve()

    def dispatch(self, commands: Set[Command]) -> NoReturn:
        """
        Indirection layer to publish messages to the publisher (infrastructure
        implementation), specifically Command messages.

        :param commands: Set of Command messages to be dispatched.
        """
        self.publisher.dispatch(commands)
