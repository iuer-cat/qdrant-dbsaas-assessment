from pydantic import field_validator

from nexus.core.infrastructure.model.pydantic.pydantic_model import \
    PydanticModel, PydanticNonSerializableModel

# NOTE: Reused Code From other personal works, Take it as leverage rather tha
# a feature.

domain_field_validator: object = field_validator

SerializableModel: object = PydanticModel
NonSerializableModel: object = PydanticNonSerializableModel
ConfigModel: object = PydanticNonSerializableModel

ValueObject: object = PydanticModel
Entity: object = PydanticModel

"""
DTOs are a core concept in many architectural patterns, used to transfer
data between software application subsystems or layers. They are
particularly important in decoupling the core business logic of an
application from its external interfaces, such as databases, web interfaces,
or external APIs.

In the context of a service bus system, DTOs serve as structured data
containers for messages, commands, queries, or events. These objects are
serializable, meaning they can be converted to and from formats suitable
for network transmission or storage, concretely to JSON and Python
dictionaries for our particular use cases.

A DTO, being mostly anemic, primarily carries data and exhibits minimal
behavior. This contrasts with more behavior-rich objects such as Entities
or Value Objects in Domain-Driven Design (DDD).

.. note::
    For further reading:
    - Data Transfer Object Pattern: https://en.wikipedia.org/wiki/Data_transfer_object
    - Ports and Adapters Architecture: https://en.wikipedia.org/wiki/Hexagonal_architecture_(software)
    - Anemic Domain Model: https://martinfowler.com/bliki/AnemicDomainModel.html
"""
ETDataTransferObject: object = PydanticModel