from abc import ABC, abstractmethod
from uuid import UUID
from src.core.role.domain.role import Role

class RoleRepository(ABC):
    @abstractmethod
    def create(self, role):
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> Role | None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self, role: Role) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> list[Role]:
        raise NotImplementedError