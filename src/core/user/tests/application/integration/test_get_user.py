from unittest.mock import create_autospec
from uuid import uuid4
from src.core.user.application.use_cases.get_user import GetUser
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository

from src.core.user.domain.user import User
from src.core.role.domain.role import Role

import pytest

@pytest.mark.user
class TestGetUser:
    def test_return_found_user(self):
        role = Role(description="Admin")

        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=role.id
            )
        repository = InMemoryUserRepository(users=[user])
        role_repository = InMemoryRoleRepository(roles=[role])


        use_case = GetUser(repository=repository, role_repository=role_repository)
        input = GetUser.Input(id=user.id)
        response = use_case.execute(input=input)

        assert response == GetUser.Output(
            id = user.id, 
            name="John",
            email="dev@email.com",
            role="Admin"

        )
    
    def test_when_user_not_found_then_raise_exception(self):
        repository = InMemoryUserRepository()
        role_repository = InMemoryRoleRepository()

        use_case = GetUser(repository=repository, role_repository=role_repository)
        request = GetUser.Input(id=uuid4())

        with pytest.raises(UserNotFound):
            use_case.execute(request)


    