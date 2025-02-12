from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.user.domain.user import User
from unittest.mock import create_autospec
import pytest
from src.core.role.domain.role_repository import RoleRepository


@pytest.mark.user
class TestUpdateUser:
    def test_update_user_from_repository(self):
        id = uuid4()
        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=uuid4()
            )

        mock_role_repository = MagicMock(RoleRepository)
        mock_claim_repository = MagicMock(ClaimRepository)

        mock_repository = create_autospec(UserRepository)

        mock_repository.get_by_id.return_value = user

        use_case = UpdateUser(repository=mock_repository, role_repository=mock_role_repository, claim_repository=mock_claim_repository)
        use_case.execute(UpdateUser.Input(id=id, email="developer@email.com"))

        mock_repository.update.assert_called_once_with(user)

    def test_update_user_when_user_not_found_then_raise_exception(self):

        mock_repository = create_autospec(UserRepository)
        mock_role_repository = MagicMock(RoleRepository)
        mock_claim_repository = MagicMock(ClaimRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateUser(repository=mock_repository, role_repository=mock_role_repository, claim_repository=mock_claim_repository)

        with pytest.raises(UserNotFound):
            use_case.execute(UpdateUser.Input(id=uuid4(), email="developer@email.com"))
        
        mock_repository.update.assert_not_called() 
        assert mock_repository.update.called is False