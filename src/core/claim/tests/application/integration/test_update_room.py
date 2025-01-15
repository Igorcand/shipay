from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.claim.application.use_cases.update_claim import UpdateClaim
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.domain.claim import Claim
from unittest.mock import create_autospec
import pytest

from src.core.claim.infra.in_memory_claim_repository import InMemoryClaimRepository

@pytest.mark.claim
class TestDeleteClaim:
    def test_update_claim_from_repository(self):
        claim = Claim(
            description="claim", 
            id=uuid4(), 
            )

        repository = InMemoryClaimRepository(claims=[claim])

        use_case = UpdateClaim(repository=repository)
        use_case.execute(UpdateClaim.Input(id=claim.id, description="claim2"))

        updated_room = repository.get_by_id(claim.id)
        assert updated_room.id == claim.id
        assert updated_room.description == "claim2"

    def test_activate_claim_from_repository(self):
        claim = Claim(
            description="claim", 
            id=uuid4(), 
            )

        repository = InMemoryClaimRepository(claims=[claim])

        use_case = UpdateClaim(repository=repository)
        use_case.execute(UpdateClaim.Input(id=claim.id, active=True))

        updated_room = repository.get_by_id(claim.id)
        assert updated_room.id == claim.id
        assert updated_room.description == "claim"
        assert updated_room.active == True

    def test_deactivate_claim_from_repository(self):
        claim = Claim(
            description="claim", 
            id=uuid4(), 
            active=True
            )

        repository = InMemoryClaimRepository(claims=[claim])

        use_case = UpdateClaim(repository=repository)
        use_case.execute(UpdateClaim.Input(id=claim.id, active=False))

        updated_room = repository.get_by_id(claim.id)
        assert updated_room.id == claim.id
        assert updated_room.description == "claim"
        assert updated_room.active == False



    def test_update_claim_when_claim_not_found_then_raise_exception(self):

        repository = InMemoryClaimRepository()

        use_case = UpdateClaim(repository=repository)

        with pytest.raises(ClaimNotFound):
            use_case.execute(UpdateClaim.Input(id=uuid4(), description="claim2"))
        