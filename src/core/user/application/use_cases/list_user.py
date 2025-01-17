from uuid import UUID
from dataclasses import dataclass, field
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository

@dataclass
class UserOutput:
    id: UUID
    name: str
    email: str
    role: str



class ListUser:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[UserOutput]

    def __init__(self, repository: UserRepository, role_repository: RoleRepository) -> None:
        self.repository = repository
        self.role_repository = role_repository

    def execute(self, input: Input) -> Output:
        users = self.repository.list()
        roles = self.role_repository.list() 
        role_descriptions = {role.id: role.description for role in roles}

        return self.Output(data = [
                UserOutput(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=role_descriptions.get(user.role_id)
                ) for user in users
            ])
    