from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user_repository import UserRepository
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

        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = user

        use_case = DeleteUser(mock_repository)
        use_case.execute(DeleteUser.Input(id=user.id))

        mock_repository.delete.assert_called_once_with(user.id)

    def test_when_link_not_found_then_raise_exception(self):
        mock_repository = create_autospec(UserRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteUser(mock_repository)

        with pytest.raises(UserNotFound):
            use_case.execute(DeleteUser.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False