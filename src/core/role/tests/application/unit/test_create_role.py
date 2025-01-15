from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.create_role import CreateRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.domain.role import Role
import pytest

@pytest.mark.role
class TestCreateRole:
    def test_create_role_with_valid_data(self):
        mock_repository = MagicMock(RoleRepository)
        use_case = CreateRole(repository=mock_repository)
        request = CreateRole.Input(
            description="Developer"
            )

        response = use_case.execute(request)

        assert response is not None
        assert isinstance(response, CreateRole.Output)
        assert isinstance(response.id, UUID)
        assert mock_repository.create.called is True
    
    def test_create_role_with_no_data_provided(self):
        mock_repository = MagicMock(RoleRepository)
        use_case = CreateRole(repository=mock_repository)
        with pytest.raises(TypeError) as exc_info:
            response = use_case.execute(CreateRole.Input())

    def test_create_role_with_invalid_data(self):
        mock_repository = MagicMock(RoleRepository)

        use_case = CreateRole(repository=mock_repository)
        with pytest.raises(InvalidRoleData, match="description cannot be empty") as exc_info:
            response = use_case.execute(CreateRole.Input(description=""))
