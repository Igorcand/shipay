from uuid import UUID
from dataclasses import dataclass, field
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository

from src.core.user.application.use_cases.exceptions import UserNotFound, InvalidUserData, RelatedRolesNotFound

class UpdateUser:
    @dataclass
    class Input:
        id: UUID
        email: str | None = None
        password: str | None = None
        role_ids: set[UUID] = field(default_factory=set)

    def __init__(self, repository: UserRepository, role_repository: RoleRepository) -> None:
        self.repository = repository
        self.role_repository = role_repository

    def execute(self, input: Input) -> None:
        user = self.repository.get_by_id(id=input.id)
        if user is None:
            raise UserNotFound(f"User with {input.id} not found")

        if input.role_ids:
            role_ids = {category.id for category in self.role_repository.list()}
            if not input.role_ids.issubset(role_ids):
                raise RelatedRolesNotFound(
                    f"Role id not found: {input.role_ids}"
                )
        
        current_email = user.email
        current_password = user.password
        current_role_ids = user.role_ids

        if input.email is not None: current_email = input.email
        
        if input.password is not None: current_password = input.password

        if input.role_ids is not None: current_role_ids = input.role_ids


        try:
            user.update_user(
                email=current_email,
                password=current_password,
                role_ids=current_role_ids
                )
        except ValueError as err:
            raise InvalidUserData(err)
    
        self.repository.update(user)
    