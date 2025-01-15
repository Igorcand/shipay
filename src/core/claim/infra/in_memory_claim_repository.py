from uuid import UUID
from src.core.claim.domain.claim import Claim
from src.core.claim.domain.claim_repository import ClaimRepository

class InMemoryClaimRepository(ClaimRepository):
    def __init__(self, claims=None) -> None:
        self.claims = claims or []
    
    def create(self, claim) -> None:
        self.claims.append(claim)
    
    def get_by_id(self, id: UUID) -> Claim | None:
        for claim in self.claims:
            if claim.id == id:
                return claim
        return None
    
    def delete(self, id: UUID) -> None:
        claim = self.get_by_id(id)
        self.claims.remove(claim)
    
    def update(self, claim: Claim) -> None:
        old_claim = self.get_by_id(claim.id)
        if old_claim:
            self.claims.remove(old_claim)
            self.claims.append(claim)
    
    def list(self) -> list[Claim]:
        return [claim for claim in self.claims]
 