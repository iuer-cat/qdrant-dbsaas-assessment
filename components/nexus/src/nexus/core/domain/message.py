import uuid
from typing import Optional, Any, Dict

from datetime import datetime
from abc import ABC

from nexus.core.infrastructure.model.implementations import \
    ETDataTransferObject


# NOTE: Reused Code From other personal works, Take it as leverage rather tha
# a feature.

def new_uuid():
    """
    Generates a new universally unique identifier (UUID).

    :return: A new UUID as a string.
    :rtype: str
    """
    return str(uuid.uuid4())


class Message(ETDataTransferObject, ABC):
    """
    Abstract base class for Data Transfer Objects (DTOs) within the service bus
    context, capable of being published or consumed.

    Every message adheres to a set of domain-level rules, ensuring consistency
    and reliability in message handling and processing:
        - Each message must have a unique identifier, creation date, version,
          and a schema identifier for serialization and deserialization.
        - Optionally, messages can carry metadata relevant to their consumers.
        - Messages are designed to travel across systems via queues or network
          connections, thus adherence to these rules is essential.

    The class ensures that if no identifier or creation date is provided during
    instantiation, default values (a random UUID and the current timestamp) are
    assigned.

    :ivar id: The unique identifier of the message, defaults to a random UUID.
    :type id: str
    :ivar created_at: The creation timestamp of the message, defaults to the
        current time.
    :type created_at: str
    :ivar type: The type of the message.
    :type type: str
    :ivar schema_id: The identifier of the schema used for the message.
    :type schema_id: int
    :ivar metadata: Optional metadata associated with the message.
    :type metadata: Optional[Any]
    """

    id:                     str
    created_at:             str
    type:                   str
    schema_id:              int

    metadata:               Dict[str, Any]

    def __init__(self, **kwargs):
        """
        Initializes a new Message instance. Assigns a random UUID and the
        current  timestamp if 'id' and 'created_at' are not provided in the
        arguments.

        :param kwargs: Keyword arguments for message attributes.
        """
        if 'id' not in kwargs:
            kwargs['id'] = str(uuid.uuid4())
        if 'created_at' not in kwargs:
            kwargs['created_at'] = str(datetime.now())
        if 'metadata' not in kwargs:
            kwargs['metadata'] = dict()
        super(Message, self).__init__(**kwargs)

    def __hash__(self):
        """
        Generates a hash value for the Message instance based on its unique
        (Optimistically) identifier.

        :return: The hash value of the message.
        :rtype: int
        """
        return hash(self.id)
