from uuid import uuid4
from src.core.role.application.use_cases.get_role import GetRole
from src.core.role.domain.role import Role
from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository
from src.core.role.application.use_cases.exceptions import RoleNotFound
import pytest

@pytest.mark.role
class TestGetRole:
    def test_get_role_by_id(self):
        role = Role(
            description="Admin"
        )
        repository = InMemoryRoleRepository(roles=[role])
        use_case = GetRole(repository=repository)

        input = GetRole.Input(id=role.id)

        response = use_case.execute(input)

        assert response == GetRole.Output(
            id = role.id,
            description="Admin"
        )
    
    def test_when_role_does_not_exist_then_raise_exception(self):
        role = Role(
            description="Admin"
        )
        repository = InMemoryRoleRepository(roles=[role])
        use_case = GetRole(repository=repository)

        request = GetRole.Input(id=uuid4())

        with pytest.raises(RoleNotFound) as exc:
            use_case.execute(request)
