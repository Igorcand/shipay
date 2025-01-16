from uuid import UUID
from src.api.claim.model import Claim as ClaimModel
from src.core.claim.domain.claim_repository import ClaimRepository
from src.core.claim.domain.claim import Claim
from sqlalchemy.orm import Session

class SQLAlchemyClaimRepository(ClaimRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, claim: Claim) -> None:
        claim_model = ClaimModel(
            id=claim.id,
            description=claim.description,
            active=claim.active,
        )
        self.session.add(claim_model)
        self.session.commit()

    def get_by_id(self, id: UUID) -> Claim | None:
        claim_model = self.session.query(ClaimModel).filter_by(id=id).first()
        if claim_model:
            return Claim(
                id=claim_model.id,
                description=claim_model.description,
                active=claim_model.active,
            )
        return None

    def delete(self, id: UUID) -> None:
        claim_model = self.session.query(ClaimModel).filter_by(id=id).first()
        if claim_model:
            self.session.delete(claim_model)
            self.session.commit()

    def update(self, claim: Claim) -> None:
        claim_model = self.session.query(ClaimModel).filter_by(id=claim.id).first()
        if claim_model:
            claim_model.description = claim.description
            claim_model.active = claim.active
            self.session.commit()

    def list(self) -> list[Claim]:
        claim_models = self.session.query(ClaimModel).all()
        return [
            Claim(id=claim.id, description=claim.description, active=claim.active)
            for claim in claim_models
        ]