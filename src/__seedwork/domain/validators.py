from abc import ABC
from typing import Any
from dataclasses import dataclass
from __seedwork.domain.exceptions import ValidationException


@dataclass(frozen=True, slots=True)
class ValidatorRules(ABC):

    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> "ValidatorRules":
        if self.value is None or self.value == "":
            raise ValidationException(f"The {self.prop} is required")
        return self

    def string(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f"The {self.prop} must be a string")
        return self

    def max_length(self, max_length: int) -> "ValidatorRules":
        if self.value is not None and len(self.value) > max_length:
            raise ValidationException(f"The {self.prop} must be less than {max_length} characters")
        return self

    def boolean(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, bool):
            raise ValidationException(f"The {self.prop} must be a boolean")
        return self
