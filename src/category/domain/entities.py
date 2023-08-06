import uuid
from typing import Optional
from datetime import datetime
from dataclasses import dataclass, field
from __seedwork.domain.entities import Entity
from __seedwork.domain.value_objects import UniqueEntityId


@dataclass(kw_only=True, frozen=True)
class Category(Entity):

    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(
        default_factory=lambda: datetime.now()
    )
