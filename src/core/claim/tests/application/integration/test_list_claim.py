from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.list_claim import ListClaim, ClaimOutput
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.domain.claim import Claim
from unittest.mock import create_autospec
import pytest

from src.core.claim.infra.in_memory_claim_repository import InMemoryClaimRepository

@pytest.mark.claim
class TestListClaim:
    def test_when_no_claims_in_repository_then_return_empty_list(self):
        repository = InMemoryClaimRepository()

        use_case = ListClaim(repository=repository)
        response = use_case.execute(ListClaim.Input())

        assert response == ListClaim.Output(
            data=[]
            )
    
    def test_when_claims_in_repository_then_return_list(self):
        claim = Claim(
            description="claim", 
            id=uuid4(), 
        )
        repository = InMemoryClaimRepository(claims=[claim])

        use_case = ListClaim(repository=repository)
        response = use_case.execute(ListClaim.Input())

        assert response == ListClaim.Output(
            data=[
                ClaimOutput(
                    id=claim.id,
                    description=claim.description,
                    active=claim.active
                ),
            ]
        )
    