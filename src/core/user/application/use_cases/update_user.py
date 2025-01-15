from uuid import UUID
from dataclasses import dataclass
from src.core.user.domain.user_repository import UserRepository
from src.core.user.application.use_cases.exceptions import UserNotFound, InvalidUserData

class UpdateUser:
    @dataclass
    class Input:
        id: UUID
        email: str | None = None
        password: str | None = None
        role_id: UUID | None = None

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> None:
        user = self.repository.get_by_id(id=input.id)
        if user is None:
            raise UserNotFound(f"User with {input.id} not found")

        current_email = user.email
        current_password = user.password
        current_role_id = user.role_id

        if input.email is not None: current_email = input.email
        
        if input.password is not None: current_password = input.password

        if input.role_id is not None: current_role_id = input.role_id


        try:
            user.update_user(
                email=current_email,
                password=current_password,
                role_id=current_role_id
                )
        except ValueError as err:
            raise InvalidUserData(err)
    
        self.repository.update(user)
    