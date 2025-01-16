from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.list_user import ListUser, UserOutput
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from unittest.mock import create_autospec
import pytest

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository

@pytest.mark.user
class TestListUser:
    def test_when_no_users_in_repository_then_return_empty_list(self):
        repository = InMemoryUserRepository()

        use_case = ListUser(repository=repository)
        response = use_case.execute(ListUser.Input())

        assert response == ListUser.Output(
            data=[]
            )
    
    def test_when_users_in_repository_then_return_list(self):
        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_ids={uuid4()}
            )
        repository = InMemoryUserRepository(users=[user])

        use_case = ListUser(repository=repository)
        response = use_case.execute(ListUser.Input())

        assert response == ListUser.Output(
            data=[
                UserOutput(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role_ids=user.role_ids,

                ),
            ]
        )
    