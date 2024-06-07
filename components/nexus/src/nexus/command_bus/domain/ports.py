from abc import ABC
from typing import List, Set, NoReturn

from nexus.core.domain.command import Command


class CommandSubscriber(ABC):
    """
    DDD Port responsible for defining the contract for MessageBroker
    implementations for the command bus, specifically for all message
    consumption operations.
    """

    def retrieve(self) -> List[Command]:
        """
        Retrieves a list of Command messages from the message broker.

        :return: List of Command messages.
        """
        raise NotImplementedError()


class CommandPublisher(ABC):
    """
    DDD Port responsible for defining the contract for MessageBroker
    implementations for the command bus, specifically for all message publishing
    operations.
    """

    def dispatch(self, commands: Set[Command]) -> NoReturn:
        """
        Dispatches a set of Command messages to the message broker.

        :param commands: Set of Command messages to be dispatched.
        """
        raise NotImplementedError()