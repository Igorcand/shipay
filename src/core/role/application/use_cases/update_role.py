from uuid import UUID
from dataclasses import dataclass
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.application.use_cases.exceptions import RoleNotFound, InvalidRoleData

class UpdateRole:
    @dataclass
    class Input:
        id: UUID
        description: str

    def __init__(self, repository: RoleRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> None:
        role = self.repository.get_by_id(id=input.id)
        if role is None:
            raise RoleNotFound(f"Role with {input.id} not found")

        try:
            role.update_role(
                description=input.description,
                )
        except ValueError as err:
            raise InvalidRoleData(err)
    
        self.repository.update(role)
    