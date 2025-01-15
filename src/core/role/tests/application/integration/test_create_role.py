from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.create_role import CreateRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData

from src.core.role.domain.role_repository import RoleRepository

from src.core.role.domain.role import Role

from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository



import pytest

@pytest.mark.role
class TestCreateRole:
    def test_create_role_with_valid_data(self):
        repository = InMemoryRoleRepository()

        use_case = CreateRole(repository=repository)
        request = CreateRole.Input(
            description="Developer"
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateRole.Output)
        assert isinstance(response.id, UUID)
    
    def test_create_role_with_invalid_data(self):
        repository = InMemoryRoleRepository()
        use_case = CreateRole(repository=repository)

        with pytest.raises(InvalidRoleData, match="description cannot be empty") as exc_info:
            response = use_case.execute(CreateRole.Input(description=""))
    
    