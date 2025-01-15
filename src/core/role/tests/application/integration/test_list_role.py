from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.list_role import ListRole, RoleOutput
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.domain.role import Role
from unittest.mock import create_autospec
import pytest

from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository

@pytest.mark.role
class TestListRole:
    def test_when_no_roles_in_repository_then_return_empty_list(self):
        repository = InMemoryRoleRepository()

        use_case = ListRole(repository=repository)
        response = use_case.execute(ListRole.Input())

        assert response == ListRole.Output(
            data=[]
            )
    
    def test_when_roles_in_repository_then_return_list(self):
        role = Role(
            description="Developer", 
            id=uuid4(), 
        )
        repository = InMemoryRoleRepository(roles=[role])

        use_case = ListRole(repository=repository)
        response = use_case.execute(ListRole.Input())

        assert response == ListRole.Output(
            data=[
                RoleOutput(
                    id=role.id,
                    description=role.description,
                ),
            ]
        )
    