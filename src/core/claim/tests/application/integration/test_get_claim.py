from uuid import uuid4
from src.core.claim.application.use_cases.get_claim import GetClaim
from src.core.claim.domain.claim import Claim
from src.core.claim.infra.in_memory_claim_repository import InMemoryClaimRepository
from src.core.claim.application.use_cases.exceptions import ClaimNotFound
import pytest

@pytest.mark.claim
class TestGetClaim:
    def test_get_claim_by_id(self):
        claim = Claim(
            description="Admin"
        )
        repository = InMemoryClaimRepository(claims=[claim])
        use_case = GetClaim(repository=repository)

        input = GetClaim.Input(id=claim.id)

        response = use_case.execute(input)

        assert response == GetClaim.Output(
            id = claim.id,
            description="Admin",
            active=False
        )
    
    def test_when_claim_does_not_exist_then_raise_exception(self):
        claim = Claim(
            description="Admin"
        )
        repository = InMemoryClaimRepository(claims=[claim])
        use_case = GetClaim(repository=repository)

        request = GetClaim.Input(id=uuid4())

        with pytest.raises(ClaimNotFound) as exc:
            use_case.execute(request)
