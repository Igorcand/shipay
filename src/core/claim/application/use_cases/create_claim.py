from uuid import UUID
from dataclasses import dataclass
from src.core.claim.application.use_cases.exceptions import InvalidClaimData
from src.core.claim.domain.claim_repository import ClaimRepository

from src.core.claim.domain.claim import Claim

class CreateClaim:
    def __init__(self, repository: ClaimRepository) -> None:
        self.repository = repository

    @dataclass
    class Input:
        description: str
        active: bool = False


    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        try:
            claim = Claim(
                description = input.description,
                active=input.active
            )
        except ValueError as e:
            raise InvalidClaimData(e)
        
        self.repository.create(claim)
        return self.Output(id=claim.id)