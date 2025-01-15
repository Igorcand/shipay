from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.delete_claim import DeleteClaim
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.infra.in_memory_claim_repository import InMemoryClaimRepository
from src.core.claim.domain.claim import Claim
from unittest.mock import create_autospec
import pytest

@pytest.mark.claim
class TestDeleteClaim:
    def test_delete_claim_from_repository(self):
        claim = Claim(
            description="claim", 
            id=uuid4(), 
        )
        repository = InMemoryClaimRepository(claims=[claim])

        use_case = DeleteClaim(repository=repository)
        request = use_case.execute(DeleteClaim.Input(id=claim.id))

        assert repository.get_by_id(claim.id) is None
        assert request is None

    def test_when_claim_not_found_then_raise_exception(self):
        repository = InMemoryClaimRepository()

        use_case = DeleteClaim(repository)

        with pytest.raises(ClaimNotFound):
            use_case.execute(DeleteClaim.Input(id=uuid4()))
        