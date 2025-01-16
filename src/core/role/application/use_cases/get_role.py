from uuid import UUID
from dataclasses import dataclass
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.application.use_cases.exceptions import RoleNotFound




class GetRole:
    def __init__(self, repository: RoleRepository) -> None:
        self.repository = repository
    
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        description: str

    def execute(self, input: Input) -> Output:

        role = self.repository.get_by_id(id=input.id)

        if role is None:
            raise RoleNotFound(f"Role with id {input.id} not found")

        return self.Output(
            id=role.id,
            description=role.description,
            )
    