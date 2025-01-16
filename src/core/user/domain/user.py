from dataclasses import dataclass, field
from uuid import UUID, uuid4
from typing import Set

@dataclass
class User():
    name : str
    email : str
    password : str | None = None
    role_ids : set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if not self.email:
            raise ValueError("email cannot be empty")
        
        if not self.name:
            raise ValueError("name cannot be empty")
        
        if len(self.email) > 255:
            raise ValueError("email cannot be longer than 255")
        
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255")
    
    def update_user(self, email: str, password: str, role_ids: Set[UUID]):
        self.email = email
        self.password = password
        self.role_ids = role_ids

        self.validate()

    def __str__(self):
        return f"{self.id} - {self.email}"
    
    def __repr__(self) -> str:
        return f"User ({self.id})"

