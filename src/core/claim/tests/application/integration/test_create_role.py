from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.create_claim import CreateClaim
from src.core.claim.application.use_cases.exceptions import InvalidClaimData

from src.core.claim.domain.claim_repository import ClaimRepository

from src.core.claim.domain.claim import Claim

from src.core.claim.infra.in_memory_claim_repository import InMemoryClaimRepository



import pytest

@pytest.mark.claim
class TestCreateClaim:
    def test_create_claim_with_valid_data(self):
        repository = InMemoryClaimRepository()

        use_case = CreateClaim(repository=repository)
        request = CreateClaim.Input(
            description="claim"
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateClaim.Output)
        assert isinstance(response.id, UUID)
    
    def test_create_claim_with_invalid_data(self):
        repository = InMemoryClaimRepository()
        use_case = CreateClaim(repository=repository)

        with pytest.raises(InvalidClaimData, match="description cannot be empty") as exc_info:
            response = use_case.execute(CreateClaim.Input(description=""))
    
    