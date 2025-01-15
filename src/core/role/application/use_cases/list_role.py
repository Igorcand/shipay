from uuid import UUID
from dataclasses import dataclass, field
from src.core.role.domain.role import Role
from src.core.role.domain.role_repository import RoleRepository

@dataclass
class RoleOutput:
    id: UUID
    description: str

class ListRole:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[RoleOutput]

    def __init__(self, repository: RoleRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> Output:
        roles = self.repository.list()

        return self.Output(data = [
                RoleOutput(
                    id=role.id,
                    description=role.description,
                ) for role in roles
            ])
    