from uuid import UUID
from src.api.user.model import User as UserModel
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
        self.session.commit()

    def get_by_id(self, id: UUID) -> User | None:
        user_model = self.session.query(UserModel).filter_by(id=id).first()
        if user_model:
            return User(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                role_id=user_model.role_id,
                password=user_model.password,
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
            self.session.commit()

    def list(self) -> list[User]:
        user_models = self.session.query(UserModel).all()
        return [
            User(id=user.id, name=user.name, email=user.email,role_id=user.role_id , password=user.password)
            for user in user_models
        ]