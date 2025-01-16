from unittest.mock import create_autospec
from uuid import uuid4
from src.core.role.application.use_cases.get_role import GetRole
from src.core.role.application.use_cases.exceptions import RoleNotFound
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.domain.role import Role
import pytest

@pytest.mark.role
class TestGetRole:
    def test_return_found_role(self):
        role = Role(
            description="Admin", 
        )
        mock_repository = create_autospec(RoleRepository)
        mock_repository.get_by_id.return_value = role

        use_case = GetRole(repository=mock_repository)
        input = GetRole.Input(id=role.id)
        response = use_case.execute(input=input)

        assert response == GetRole.Output(
            id = role.id, 
            description="Admin"

        )
    
    def test_when_role_not_found_then_raise_exception(self):
        mock_repository = create_autospec(RoleRepository)
        mock_repository.get_by_id.return_value = None

        use_case = GetRole(repository=mock_repository)
        request = GetRole.Input(id=uuid4())

        with pytest.raises(RoleNotFound):
            use_case.execute(request)


    