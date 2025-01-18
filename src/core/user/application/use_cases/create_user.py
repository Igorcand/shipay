import random
import string
from uuid import UUID
from dataclasses import dataclass, field
from src.core.user.application.use_cases.exceptions import InvalidUserData, RelatedRolesNotFound, RelatedClaimNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.role.domain.role_repository import RoleRepository
from src.core.claim.domain.claim_repository import ClaimRepository



from src.core.user.domain.user import User

class CreateUser:
    def __init__(self, repository: UserRepository, role_repository: RoleRepository, claim_repository: ClaimRepository) -> None:
        self.repository = repository
        self.role_repository = role_repository
        self.claim_repository=claim_repository

    @dataclass
    class Input:
        name: str
        email: str
        role_id: UUID
        claim_ids : set[UUID] = field(default_factory=set)
        password: str | None = None


    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input):
        try:

            role_ids = {category.id for category in self.role_repository.list()}
            if input.role_id not in role_ids:
                raise RelatedRolesNotFound(
                    f"Role id not found: {input.role_id}"
                )
            
            claim_ids = {claim.id for claim in self.claim_repository.list()}
            if not input.claim_ids.issubset(claim_ids):
                raise RelatedClaimNotFound(
                    f"Claims Id not found: {input.claim_ids - claim_ids}"
                )
            
            if not input.password:
                caracteres = string.ascii_letters + string.digits + string.punctuation
                input.password =  ''.join(random.choice(caracteres) for _ in range(12))
                
            user = User(
                name=input.name,
                email=input.email,
                role_id=input.role_id,
                password=input.password,
                claim_ids=input.claim_ids
            )
        except ValueError as e:
            raise InvalidUserData(e)
        
        self.repository.create(user)
        return self.Output(id=user.id)