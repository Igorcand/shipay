from uuid import UUID
from dataclasses import dataclass, field
from src.core.claim.domain.claim import Claim
from src.core.claim.domain.claim_repository import ClaimRepository

@dataclass
class ClaimOutput:
    id: UUID
    description: str
    active: bool

class ListClaim:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[ClaimOutput]

    def __init__(self, repository: ClaimRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> Output:
        claims = self.repository.list()

        return self.Output(data = [
                ClaimOutput(
                    id=claim.id,
                    description=claim.description,
                    active=claim.active,
                ) for claim in claims
            ])
    