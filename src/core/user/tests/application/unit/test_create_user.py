from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository
from src.core.claim.domain.claim_repository import ClaimRepository


from src.core.role.domain.role import Role
from src.core.claim.domain.claim import Claim

import pytest

@pytest.mark.user
class TestCreateUser:
    def test_create_user_with_valid_data(self):
        mock_repository = MagicMock(UserRepository)
        mock_role_repository = MagicMock(RoleRepository)
        mock_claim_repository = MagicMock(ClaimRepository)

        role = Role(description="Admin")
        claim = Claim(description="claim")

        mock_role_repository.list.return_value = [role]
        mock_claim_repository.list.return_value = [claim]


        use_case = CreateUser(repository=mock_repository, role_repository=mock_role_repository, claim_repository=mock_claim_repository)
        request = CreateUser.Input(
            name="John",
            email="dev@email.com",
            role_id=role.id,
            claim_ids={claim.id},
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateUser.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True
    
    def test_create_user_with_no_data_provided(self):
        mock_repository = MagicMock(UserRepository)
        mock_role_repository = MagicMock(RoleRepository)
        mock_claim_repository = MagicMock(ClaimRepository)
        
        use_case = CreateUser(repository=mock_repository, role_repository=mock_role_repository, claim_repository=mock_claim_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreateUser.Input())


