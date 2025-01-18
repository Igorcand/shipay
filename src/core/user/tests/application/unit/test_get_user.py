from unittest.mock import create_autospec
from uuid import uuid4
from src.core.user.application.use_cases.get_user import GetUser
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository
from src.core.claim.domain.claim_repository import ClaimRepository

from src.core.user.domain.user import User
from src.core.role.domain.role import Role
from src.core.claim.domain.claim import Claim

import pytest

@pytest.mark.user
class TestGetUser:
    def test_return_found_user(self):
        role = Role(description="Admin")
        claim = Claim(description="Claim")

        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=role.id,
            claim_ids={claim.id}
            )
        mock_repository = create_autospec(UserRepository)
        mock_role_repository = create_autospec(RoleRepository)
        mock_claim_repository = create_autospec(ClaimRepository)

        mock_repository.get_by_id.return_value = user
        mock_role_repository.get_by_id.return_value = role
        mock_claim_repository.list.return_value = [claim]


        use_case = GetUser(repository=mock_repository, role_repository=mock_role_repository, claim_repository=mock_claim_repository)
        input = GetUser.Input(id=user.id)
        response = use_case.execute(input=input)

        assert response == GetUser.Output(
            id = user.id, 
            name="John",
            email="dev@email.com",
            role="Admin",
            claims={"Claim"},
        )
    
    def test_when_user_not_found_then_raise_exception(self):
        mock_repository = create_autospec(UserRepository)
        mock_role_repository = create_autospec(RoleRepository)
        mock_claim_repository = create_autospec(ClaimRepository)

        mock_repository.get_by_id.return_value = None

        use_case = GetUser(repository=mock_repository, role_repository=mock_role_repository, claim_repository=mock_claim_repository)
        request = GetUser.Input(id=uuid4())

        with pytest.raises(UserNotFound):
            use_case.execute(request)


    