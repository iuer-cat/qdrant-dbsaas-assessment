from typing import Dict, Any
from pydantic import BaseModel

# NOTE: Reused Code From other personal works, Take it as leverage rather tha
# a feature.


class PydanticModel(BaseModel):
    """
    Class encapsulating Pydantic library functionality for decoupling it from
    the domain code.
    """

    class Config:
        """
        Configuration for BaseModel.

        Attributes:
        -----------
        arbitrary_types_allowed: bool
            Whether arbitrary types are allowed for field types. Forced
            to not allow arbitrary types in our domain model objects.
        """
        arbitrary_types_allowed = False

    def as_dict(self) -> Dict[str, Any]:
        """
        Converts the Pydantic model instance into a dictionary.

        This method acts as a wrapper around Pydantic's internal serialization
        mechanism, enabling the conversion of a model instance into a
        dictionary format.

        :return: A dictionary representation of the model.
        """
        return self.model_dump()


class PydanticNonSerializableModel(BaseModel):
    """
    Class encapsulating Pydantic library functionality for decoupling it from
    the domain code.

    This class try to emulate the dataclass capabilities but taking advantage of
    the validation schemas presents in Pydantic.
    """

    class Config:
        """
        Configuration for PydanticNonSerializableModel.

        Attributes:
        -----------
        arbitrary_types_allowed: bool
            A configuration setting that allows for arbitrary types within the
            model. Used basically for internal data models where we still
            want some capabilities of pydantic but not the enforcing of data
            types.
        """
        arbitrary_types_allowed = True

    def as_dict(self) -> Dict[str, Any]:
        """
        Converts the Pydantic model instance into a dictionary.

        This method acts as a wrapper around Pydantic's internal serialization
        mechanism, enabling the conversion of a model instance into a
        dictionary format.

        :return: A dictionary representation of the model.
        """
        return self.model_dump()