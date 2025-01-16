from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.delete_claim import DeleteClaim
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository
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

        mock_repository = create_autospec(ClaimRepository)
        mock_repository.get_by_id.return_value = claim

        use_case = DeleteClaim(mock_repository)
        use_case.execute(DeleteClaim.Input(id=claim.id))

        mock_repository.delete.assert_called_once_with(claim.id)

    def test_when_link_not_found_then_raise_exception(self):
        mock_repository = create_autospec(ClaimRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteClaim(mock_repository)

        with pytest.raises(ClaimNotFound):
            use_case.execute(DeleteClaim.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False