from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from __seedwork.domain.entities import Entity


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )

    def update(self, name: str, description: Optional[str] = None) -> None:
        value = description \
            if description is not None \
            else self.description
        self._set("name", name)
        self._set("description", value)

    def activate(self) -> None:
        self._set("is_active", True)

    def deactivate(self) -> None:
        self._set("is_active", False)
