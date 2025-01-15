from uuid import UUID
from dataclasses import dataclass
from src.core.role.application.use_cases.exceptions import InvalidRoleData
from src.core.role.domain.role_repository import RoleRepository

from src.core.role.domain.role import Role

class CreateRole:
    def __init__(self, repository: RoleRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        description: str

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        try:
            role = Role(
                description = input.description,
            )
        except ValueError as e:
            raise InvalidRoleData(e)
        
        self.repository.create(role)
        return self.Output(id=role.id)