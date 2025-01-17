from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.list_user import ListUser, UserOutput
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user import User
from unittest.mock import create_autospec
import pytest
from src.core.role.domain.role import Role
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository


@pytest.mark.user
class TestListUser:
    def test_when_no_users_in_repository_then_return_empty_list(self):
        repository = InMemoryUserRepository()
        role_repository = InMemoryRoleRepository()

        use_case = ListUser(repository=repository, role_repository=role_repository)
        response = use_case.execute(ListUser.Input())

        assert response == ListUser.Output(
            data=[]
            )
    
    def test_when_users_in_repository_then_return_list(self):
        role = Role(description="Admin")
        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=role.id
            )
        repository = InMemoryUserRepository(users=[user])
        role_repository = InMemoryRoleRepository(roles=[role])

        use_case = ListUser(repository=repository, role_repository=role_repository)
        response = use_case.execute(ListUser.Input())

        assert response == ListUser.Output(
            data=[
                UserOutput(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=role.description,

                ),
            ]
        )
    