from uuid import UUID
from dataclasses import dataclass
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.application.use_cases.exceptions import ClaimNotFound, InvalidClaimData

class UpdateClaim:
    @dataclass
    class Input:
        id: UUID
        description: str | None = None
        active: bool | None = None

    def __init__(self, repository: ClaimRepository) -> None:
        self.repository = repository

    def execute(self, input: Input) -> None:
        claim = self.repository.get_by_id(id=input.id)
        if claim is None:
            raise ClaimNotFound(f"Claim with {input.id} not found")

        current_description = claim.description
        if input.description is not None: current_description = input.description

        try:
            claim.update_claim(
                description=current_description,
                )
        except ValueError as err:
            raise InvalidClaimData(err)
        
        if input.active is not None: 
            if input.active == True:
                claim.activate()
            else:
                claim.deactivate()
    
        self.repository.update(claim)
    