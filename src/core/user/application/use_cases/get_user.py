from uuid import UUID
from dataclasses import dataclass
from src.core.user.application.use_cases.exceptions import UserNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository
from src.core.claim.domain.claim_repository import ClaimRepository
from typing import List

class GetUser:
    def __init__(self, repository: UserRepository, role_repository: RoleRepository, claim_repository: ClaimRepository) -> None:
        self.repository = repository
        self.role_repository = role_repository
        self.claim_repository = claim_repository


    @dataclass
    class Input:
        id: UUID
    
    @dataclass
    class Output:
        id: UUID
        name: str
        email: str
        role: str
        claims: set[str]

    def execute(self, input: Input):
        user = self.repository.get_by_id(input.id)
        if user is None:
            raise UserNotFound(f"User with {input.id} not found")
        
        role = self.role_repository.get_by_id(user.role_id)

        claims = self.claim_repository.list() 
        claims_descriptions = {claim.id: claim.description for claim in claims}

        return self.Output(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=role.description,
                    claims={claims_descriptions.get(claim_id) for claim_id in user.claim_ids }
            )