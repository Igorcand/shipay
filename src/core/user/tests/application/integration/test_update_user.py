from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from unittest.mock import create_autospec
import pytest

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository

@pytest.mark.user
class TestDeleteUser:
    def test_update_user_from_repository(self):
        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=uuid4()
            )

        repository = InMemoryUserRepository(users=[user])

        use_case = UpdateUser(repository=repository)
        new_role_id = uuid4()
        use_case.execute(UpdateUser.Input(id=user.id, email="developer@email.com", password="123", role_id=new_role_id))

        updated_user = repository.get_by_id(user.id)
        assert updated_user.id == user.id
        assert updated_user.email == "developer@email.com"
        assert updated_user.password == "123"
        assert updated_user.role_id == new_role_id



    def test_update_user_when_user_not_found_then_raise_exception(self):

        repository = InMemoryUserRepository()

        use_case = UpdateUser(repository=repository)

        with pytest.raises(UserNotFound):
            use_case.execute(UpdateUser.Input(id=uuid4(), email="developer@email.com"))
        