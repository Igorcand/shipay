from uuid import UUID
from dataclasses import dataclass
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.application.use_cases.exceptions import ClaimNotFound


class GetClaim:
    def __init__(self, repository: ClaimRepository) -> None:
        self.repository = repository
    
    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        description: str
        active: bool


    def execute(self, input: Input) -> Output:

        claim = self.repository.get_by_id(id=input.id)

        if claim is None:
            raise ClaimNotFound(f"Claim with id {input.id} not found")

        return self.Output(
            id=claim.id,
            description=claim.description,
            active=claim.active,
            )
    