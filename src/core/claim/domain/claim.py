from dataclasses import dataclass, field
from uuid import UUID, uuid4

@dataclass
class Claim():
    description : str
    active : bool = False
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate()
    
    def validate(self):
        if not self.description:
            raise ValueError("description cannot be empty")
        
        if len(self.description) > 255:
            raise ValueError("description cannot be longer than 255")
    
    def update_claim(self, description: str):
        self.description = description

        self.validate()

    def activate(self):
        self.active = True

        self.validate()
    
    def deactivate(self):
        self.active = False

        self.validate()

    def __str__(self):
        return f"{self.id} - {self.description}"
    
    def __repr__(self) -> str:
        return f"Claim ({self.id})"

