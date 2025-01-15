from uuid import UUID
from src.core.role.domain.role import Role
from src.core.role.domain.role_repository import RoleRepository

class InMemoryRoleRepository(RoleRepository):
    def __init__(self, roles=None) -> None:
        self.roles = roles or []
    
    def create(self, role) -> None:
        self.roles.append(role)
    
    def get_by_id(self, id: UUID) -> Role | None:
        for role in self.roles:
            if role.id == id:
                return role
        return None
    
    def delete(self, id: UUID) -> None:
        role = self.get_by_id(id)
        self.roles.remove(role)
    
    def update(self, role: Role) -> None:
        old_room = self.get_by_id(role.id)
        if old_room:
            self.roles.remove(old_room)
            self.roles.append(role)
    
    def list(self) -> list[Role]:
        return [role for role in self.roles]
 