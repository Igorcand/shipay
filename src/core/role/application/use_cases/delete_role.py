from uuid import UUID
from dataclasses import dataclass
from src.core.role.application.use_cases.exceptions import RoleNotFound
from src.core.role.domain.role_repository import RoleRepository

class DeleteRole:
    def __init__(self, repository: RoleRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input):
        role = self.repository.get_by_id(input.id)
        if role is None:
            raise RoleNotFound(f"Role with {input.id} not found")
        self.repository.delete(role.id)