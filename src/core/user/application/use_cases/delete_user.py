from uuid import UUID
from dataclasses import dataclass
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.domain.user_repository import UserRepository

class DeleteUser:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input):
        user = self.repository.get_by_id(input.id)
        if user is None:
            raise UserNotFound(f"User with {input.id} not found")
        self.repository.delete(user.id)