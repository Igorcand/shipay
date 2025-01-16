from unittest.mock import create_autospec
from uuid import uuid4
from src.core.claim.application.use_cases.get_claim import GetClaim
from src.core.claim.application.use_cases.exceptions import ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.domain.claim import Claim
import pytest

@pytest.mark.claim
class TestGetClaim:
    def test_return_found_claim(self):
        claim = Claim(
            description="Admin", 
        )
        mock_repository = create_autospec(ClaimRepository)
        mock_repository.get_by_id.return_value = claim

        use_case = GetClaim(repository=mock_repository)
        input = GetClaim.Input(id=claim.id)
        response = use_case.execute(input=input)

        assert response == GetClaim.Output(
            id = claim.id, 
            description="Admin",
            active=False

        )
    
    def test_when_claim_not_found_then_raise_exception(self):
        mock_repository = create_autospec(ClaimRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetClaim(repository=mock_repository)
        request = GetClaim.Input(id=uuid4())

        with pytest.raises(ClaimNotFound):
            use_case.execute(request)


    