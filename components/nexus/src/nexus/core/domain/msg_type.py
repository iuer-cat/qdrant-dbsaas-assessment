from enum import Enum


# NOTE: Reused Code From other personal works, Take it as leverage rather tha
# a feature.

class MessageType(Enum):
    """
    Enumerates the different types of messages recognized in a distributed
    system utilizing a service bus. These message types are agreed upon at a
    company level to define the scope and semantics of each message.

    Typifying messages aids in understanding their intended scope and role
    within distributed systems. This classification provides clear semantics
    to developers familiar with mainstream patterns and architectures for
    distributed systems.

    The message types include:
    - `COMMAND`: Represents a mutable action that will induce a state change.

    Understanding these types allows developers to better comprehend and handle
    the flow and processing of messages in the system.

    :ivar COMMAND: Represents a command message.
    """
    COMMAND:    str = 'COMMAND'
