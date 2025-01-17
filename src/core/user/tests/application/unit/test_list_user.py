from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.list_user import ListUser, UserOutput
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository
from src.core.user.domain.user import User
from src.core.role.domain.role import Role

from unittest.mock import create_autospec
import pytest


@pytest.mark.user
class TestListUser:
    def test_when_no_users_in_repository_then_return_empty_list(self):
        mock_repository = create_autospec(UserRepository)
        mock_role_repository = create_autospec(RoleRepository)

        mock_repository.list.return_value = []

        use_case = ListUser(repository=mock_repository, role_repository=mock_role_repository)
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
        mock_repository = create_autospec(UserRepository)
        mock_role_repository = create_autospec(RoleRepository)
        mock_repository.list.return_value = [user]
        mock_role_repository.list.return_value = [role]


        use_case = ListUser(repository=mock_repository, role_repository=mock_role_repository)
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
    