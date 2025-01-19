from uuid import UUID
from src.api.user.model import User as UserModel
from src.api.user.model import UserClaim
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from sqlalchemy.orm import Session

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> None:
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=user.email,
            password=user.password,
            role_id=user.role_id,
        )
        self.session.add(user_model)

        # Adiciona as claims na tabela intermediária
        for claim_id in user.claim_ids:
            user_claim = UserClaim(user_id=user.id, claim_id=claim_id)
            self.session.add(user_claim)

        self.session.commit()

    def get_by_id(self, id: UUID) -> User | None:
        user_model = self.session.query(UserModel).filter_by(id=id).first()
        if user_model:
            claim_ids = {
                claim.claim_id for claim in self.session.query(UserClaim).filter_by(user_id=id).all()
            }
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                role_id=user_model.role_id,
                password=user_model.password,
                claim_ids=claim_ids,
            )
        return None

    def delete(self, id: UUID) -> None:
        user_model = self.session.query(UserModel).filter_by(id=id).first()
        if user_model:
            self.session.delete(user_model)
            self.session.commit()

    def update(self, user: User) -> None:
        user_model = self.session.query(UserModel).filter_by(id=user.id).first()
        if user_model:
            user_model.email = user.email
            user_model.password = user.password
            user_model.role_id = user.role_id

            # Atualiza as claims associadas
            self.session.query(UserClaim).filter_by(user_id=user.id).delete()
            for claim_id in user.claim_ids:
                user_claim = UserClaim(user_id=user.id, claim_id=claim_id)
                self.session.add(user_claim)

            self.session.commit()

    def list(self) -> list[User]:
        user_models = self.session.query(UserModel).all()
        users = []
        for user_model in user_models:
            # Obtém as claims associadas a cada usuário
            claim_ids = {
                claim.claim_id for claim in self.session.query(UserClaim).filter_by(user_id=user_model.id).all()
            }
            users.append(
                User(
                    id=user_model.id,
                    name=user_model.name,
                    email=user_model.email,
                    role_id=user_model.role_id,
                    password=user_model.password,
                    claim_ids=claim_ids,
                )
            )
        return users