from uuid import UUID
from src.api.role.model import Role as RoleModel
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.domain.role import Role
from sqlalchemy.orm import Session

class SQLAlchemyRoleRepository(RoleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, role: Role) -> None:
        role_model = RoleModel(
            id=role.id,
            description=role.description
        )
        self.session.add(role_model)
        self.session.commit()

    def get_by_id(self, id: UUID) -> Role | None:
        role_model = self.session.query(RoleModel).filter_by(id=id).first()
        if role_model:
            return Role(
                id=role_model.id,
                description=role_model.description
            )
        return None

    def delete(self, id: UUID) -> None:
        role_model = self.session.query(RoleModel).filter_by(id=id).first()
        if role_model:
            self.session.delete(role_model)
            self.session.commit()

    def update(self, role: Role) -> None:
        role_model = self.session.query(RoleModel).filter_by(id=role.id).first()
        if role_model:
            role_model.description = role.description
            self.session.commit()

    def list(self) -> list[Role]:
        role_models = self.session.query(RoleModel).all()
        return [
            Role(id=role.id, description=role.description)
            for role in role_models
        ]