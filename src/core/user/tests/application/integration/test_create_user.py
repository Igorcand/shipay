from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData, RelatedRolesNotFound,RelatedClaimNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role import Role
from src.core.claim.domain.claim import Claim
from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository
from src.core.claim.infra.in_memory_claim_repository import InMemoryClaimRepository


import pytest

@pytest.mark.user
class TestCreateUser:
    def test_create_user_with_valid_data(self):
        repository = InMemoryUserRepository()
        role = Role(description="Admin")
        role_repository = InMemoryRoleRepository(roles=[role])

        claim = Claim(description="Claim")
        claim_repository = InMemoryClaimRepository(claims=[claim])

        use_case = CreateUser(repository=repository, role_repository=role_repository, claim_repository=claim_repository)
        request = CreateUser.Input(
            name="John",
            email="dev@email.com",
            role_id=role.id,
            claim_ids={claim.id}
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateUser.Output)
        assert isinstance(response.id, UUID)
    
    def test_create_user_with_invalid_data(self):
        repository = InMemoryUserRepository()
        role = Role(description="Admin")
        role_repository = InMemoryRoleRepository(roles=[role])
        claim = Claim(description="Claim")
        claim_repository = InMemoryClaimRepository(claims=[claim])
        use_case = CreateUser(repository=repository, role_repository=role_repository, claim_repository=claim_repository)

        with pytest.raises(InvalidUserData, match="email cannot be empty") as exc_info:
            response = use_case.execute(CreateUser.Input(email="", name="John", role_id=role.id, claim_ids={claim.id}))

    def test_create_user_with_not_related_roles(self):
        repository = InMemoryUserRepository()
        role_repository = InMemoryRoleRepository()
        claim_repository = InMemoryClaimRepository()

        use_case = CreateUser(repository=repository, role_repository=role_repository, claim_repository=claim_repository)

        with pytest.raises(RelatedRolesNotFound) as exc_info:
            response = use_case.execute(CreateUser.Input(email="", name="John", role_id=uuid4(),claim_ids=set()))
    
    def test_create_user_with_not_related_claims(self):
        repository = InMemoryUserRepository()
        role = Role(description="Admin")
        role_repository = InMemoryRoleRepository(roles=[role])
        claim_repository = InMemoryClaimRepository()

        use_case = CreateUser(repository=repository, role_repository=role_repository, claim_repository=claim_repository)

        with pytest.raises(RelatedClaimNotFound) as exc_info:
            response = use_case.execute(CreateUser.Input(email="", name="John", role_id=role.id,claim_ids={uuid4()}))
    
    