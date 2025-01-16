import random
import string
from uuid import UUID
from dataclasses import dataclass
from src.core.user.application.use_cases.exceptions import InvalidUserData, RelatedRolesNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository


from src.core.user.domain.user import User

class CreateUser:
    def __init__(self, repository: UserRepository, role_repository: RoleRepository) -> None:
        self.repository = repository
        self.role_repository = role_repository

    @dataclass
    class Input:
        name: str
        email: str
        role_id: UUID
        password: str | None = None


    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        try:

            role_ids = {category.id for category in self.role_repository.list()}
            if not input.role_id in role_ids:
                raise RelatedRolesNotFound(
                    f"Role id not found: {input.role_id}"
                )
        
            if not input.password:
                caracteres = string.ascii_letters + string.digits + string.punctuation
                input.password =  ''.join(random.choice(caracteres) for _ in range(12))
                
            user = User(
                name=input.name,
                email=input.email,
                role_id=input.role_id,
                password=input.password,
            )
        except ValueError as e:
            raise InvalidUserData(e)
        
        self.repository.create(user)
        return self.Output(id=user.id)