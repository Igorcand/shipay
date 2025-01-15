from uuid import UUID
from dataclasses import dataclass
from src.core.claim.application.use_cases.exceptions import ClaimNotFound
from src.core.claim.domain.claim_repository import ClaimRepository

class DeleteClaim:
    def __init__(self, repository: ClaimRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input):
        claim = self.repository.get_by_id(input.id)
        if claim is None:
            raise ClaimNotFound(f"Claim with {input.id} not found")
        self.repository.delete(claim.id)