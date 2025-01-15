from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
import pytest

@pytest.mark.user
class TestCreateUser:
    def test_create_user_with_valid_data(self):
        repository = InMemoryUserRepository()

        use_case = CreateUser(repository=repository)
        request = CreateUser.Input(
            name="John",
            email="dev@email.com",
            role_id=uuid4()
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateUser.Output)
        assert isinstance(response.id, UUID)
    
    def test_create_user_with_invalid_data(self):
        repository = InMemoryUserRepository()
        use_case = CreateUser(repository=repository)

        with pytest.raises(InvalidUserData, match="email cannot be empty") as exc_info:
            response = use_case.execute(CreateUser.Input(email="", name="John", role_id=uuid4()))
    
    