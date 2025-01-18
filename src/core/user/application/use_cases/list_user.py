from uuid import UUID
from dataclasses import dataclass, field
from src.core.user.domain.user import User
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository
from src.core.claim.domain.claim_repository import ClaimRepository

from typing import List

@dataclass
class UserOutput:
    id: UUID
    name: str
    email: str
    role: str
    claims: set[str]

class ListUser:

    @dataclass
    class Input:
        pass
        
    @dataclass
    class Output:
        data: list[UserOutput]

    def __init__(self, repository: UserRepository, role_repository: RoleRepository, claim_repository: ClaimRepository) -> None:
        self.repository = repository
        self.role_repository = role_repository
        self.claim_repository = claim_repository

    def execute(self, input: Input) -> Output:
        users = self.repository.list()
        roles = self.role_repository.list() 
        role_descriptions = {role.id: role.description for role in roles}

        claims = self.claim_repository.list() 
        claims_descriptions = {claim.id: claim.description for claim in claims}

        return self.Output(data = [
                UserOutput(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=role_descriptions.get(user.role_id),
                    claims={claims_descriptions.get(claim_id) for claim_id in user.claim_ids }
                ) for user in users
            ])
    