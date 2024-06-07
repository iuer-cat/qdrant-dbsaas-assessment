from nexus.core.domain.message import Message
from nexus.core.domain.msg_type import MessageType
from nexus.core.infrastructure.model.implementations import \
    domain_field_validator

# NOTE: Reused Code From other personal works, Take it as leverage rather tha
# a feature.


class Command(Message):
    """
    Represents a Command Data Transfer Object (DTO) in the context of Command
    Query Responsibility Segregation (CQRS).

    Commands are messages that encapsulate an intention to perform a specific
    action. They represent the imperative nature of changing the system's state.
    In a CQRS architecture, commands are responsible for initiating changes
    in the application's data.

    A command follows a one-to-one relationship between the message producer
    and the message consumer. This one-to-one relationship simplifies the flow
    of commands, making it clear which component is responsible for handling
    a specific action.

    Commands differ from events in that they represent an intention to perform
    an action, while events represent something that has already happened.
    Commands are imperative and trigger changes, while events are declarative
    and signify state changes that have occurred. Events are often used to
    communicate these changes to other components or systems.

    Another distinction is that commands are typically directed to a specific
    handler, ensuring a clear path for execution. In contrast, events are
    broadcasted to multiple subscribers, allowing for a more decoupled and
    distributed system.

    So if you generate a command make sure there is only and only one subscriber
    associated to consume that command, and generate and event, after processing
    a command if there is other systems interested on be notified about
    this mutable action.

    Commands also allow us to decouple persistence layers, but they complicate
    the development and testability of the application. There are few reasons
    to generate commands, and most of them are usually related to performance
    in data ingestion. Commands also often bring issues of eventual
    consistency, so you must be very sure that the command is necessary, and it
    should never be the first option.

    :ivar type: The type of the message.
               Defaults to `MessageType.COMMAND.value`.
    """

    type:                   str = MessageType.COMMAND.value

    @domain_field_validator('type')
    def validate_type(
            cls,
            type: str,
    ) -> str:
        """
    Validate the 'type' field to ensure it is set to the COMMAND value defined
    in the MessageType enumeration.

    :param type: The 'type' value to validate.
    :type type: str
    :return: The original 'type' if it matches MessageType.COMMAND.value.
    :rtype: str
    :raises ValueError: If 'type' is not MessageType.COMMAND.value, indicating
        an attempt to override the default command type.
    """
        if type != MessageType.COMMAND.value:
            err_msg = f'Command Type cannot be override, should be always ' \
                      f'{MessageType.COMMAND.value}'
            raise ValueError(err_msg)

        return type

