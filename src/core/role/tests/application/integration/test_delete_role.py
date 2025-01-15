from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.delete_role import DeleteRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository
from src.core.role.domain.role import Role
from unittest.mock import create_autospec
import pytest

@pytest.mark.role
class TestDeleteRole:
    def test_delete_role_from_repository(self):
        role = Role(
            description="Developer", 
            id=uuid4(), 
        )
        repository = InMemoryRoleRepository(roles=[role])

        use_case = DeleteRole(repository=repository)
        request = use_case.execute(DeleteRole.Input(id=role.id))

        assert repository.get_by_id(role.id) is None
        assert request is None

    def test_when_role_not_found_then_raise_exception(self):
        repository = InMemoryRoleRepository()

        use_case = DeleteRole(repository)

        with pytest.raises(RoleNotFound):
            use_case.execute(DeleteRole.Input(id=uuid4()))
        