from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.update_claim import UpdateClaim
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.domain.claim import Claim
from unittest.mock import create_autospec
import pytest



@pytest.mark.claim
class TestDeleteClaim:
    def test_update_claim_from_repository(self):
        id = uuid4()
        claim = Claim(
            description="claim", 
            id=id, 
            )

        mock_repository = create_autospec(ClaimRepository)
        mock_repository.get_by_id.return_value = claim

        use_case = UpdateClaim(repository=mock_repository)
        use_case.execute(UpdateClaim.Input(id=id, description="claim2"))

        mock_repository.update.assert_called_once_with(claim)

    def test_update_claim_when_claim_not_found_then_raise_exception(self):

        mock_repository = create_autospec(ClaimRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateClaim(repository=mock_repository)

        with pytest.raises(ClaimNotFound):
            use_case.execute(UpdateClaim.Input(id=uuid4(), description="claim2"))
        
        mock_repository.update.assert_not_called() 
        assert mock_repository.update.called is False