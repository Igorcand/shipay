from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.create_claim import CreateClaim
from src.core.claim.application.use_cases.exceptions import InvalidClaimData
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.domain.claim import Claim
import pytest

@pytest.mark.claim
class TestCreateClaim:
    def test_create_claim_with_valid_data(self):
        mock_repository = MagicMock(ClaimRepository)
        use_case = CreateClaim(repository=mock_repository)
        request = CreateClaim.Input(
            description="claim"
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateClaim.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True
    
    def test_create_claim_with_no_data_provided(self):
        mock_repository = MagicMock(ClaimRepository)
        use_case = CreateClaim(repository=mock_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreateClaim.Input())

    def test_create_claim_with_invalid_data(self):
        mock_repository = MagicMock(ClaimRepository)

        use_case = CreateClaim(repository=mock_repository)
        with pytest.raises(InvalidClaimData, match="description cannot be empty") as exc_info:
            response = use_case.execute(CreateClaim.Input(description=""))
