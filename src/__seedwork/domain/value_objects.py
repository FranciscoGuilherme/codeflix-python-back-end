import uuid
from dataclasses import dataclass, field
from __seedwork.domain.exceptions import InvalidUuidException


@dataclass(frozen=True)
class UniqueEntityId:

    id: str = field(
        default_factory=lambda: str(uuid.uuid4())
    )

    def __post_init__(self) -> None:
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, "id", id_value)
        self.__validate()

    def __validate(self) -> None:
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUuidException from ex
