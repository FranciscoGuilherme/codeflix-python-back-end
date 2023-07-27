from datetime import datetime

class Category:
    def __init__(self, name: str, description: str, is_active: bool, created_at: datetime) -> None:
        self.name: str = name
        self.description: str = description
        self.is_active: bool = is_active
        self.created_at: datetime = created_at
