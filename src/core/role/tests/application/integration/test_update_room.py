from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.update_role import UpdateRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.domain.role import Role
from unittest.mock import create_autospec
import pytest

from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository

@pytest.mark.role
class TestDeleteRole:
    def test_update_role_from_repository(self):
        role = Role(
            description="Developer", 
            id=uuid4(), 
            )

        repository = InMemoryRoleRepository(roles=[role])

        use_case = UpdateRole(repository=repository)
        use_case.execute(UpdateRole.Input(id=role.id, description="Developer Sr"))

        updated_room = repository.get_by_id(role.id)
        assert updated_room.id == role.id
        assert updated_room.description == "Developer Sr"


    def test_update_role_when_role_not_found_then_raise_exception(self):

        repository = InMemoryRoleRepository()

        use_case = UpdateRole(repository=repository)

        with pytest.raises(RoleNotFound):
            use_case.execute(UpdateRole.Input(id=uuid4(), description="Developer Sr"))
        