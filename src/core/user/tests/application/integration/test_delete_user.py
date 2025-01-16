from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.user.domain.user import User
from unittest.mock import create_autospec
import pytest

@pytest.mark.user
class TestDeleteUser:
    def test_delete_user_from_repository(self):
        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_ids={uuid4()}
            )
        repository = InMemoryUserRepository(users=[user])

        use_case = DeleteUser(repository=repository)
        request = use_case.execute(DeleteUser.Input(id=user.id))

        assert repository.get_by_id(user.id) is None
        assert request is None

    def test_when_user_not_found_then_raise_exception(self):
        repository = InMemoryUserRepository()

        use_case = DeleteUser(repository)

        with pytest.raises(UserNotFound):
            use_case.execute(DeleteUser.Input(id=uuid4()))
        