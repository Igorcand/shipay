import random
import string
from uuid import UUID
from dataclasses import dataclass
from src.core.user.application.use_cases.exceptions import InvalidUserData
from src.core.user.domain.user_repository import UserRepository

from src.core.user.domain.user import User

class CreateUser:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

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