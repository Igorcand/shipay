from uuid import UUID
from dataclasses import dataclass, field
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository

@dataclass
class UserOutput:
    id: UUID
    name: str
    email: str
    role_id: UUID



class ListUser:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[UserOutput]

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> Output:
        users = self.repository.list()

        return self.Output(data = [
                UserOutput(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role_id=user.role_id,
                ) for user in users
            ])
    