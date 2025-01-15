from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.delete_role import DeleteRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from src.core.role.domain.role_repository import RoleRepository
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

        mock_repository = create_autospec(RoleRepository)
        mock_repository.get_by_id.return_value = role

        use_case = DeleteRole(mock_repository)
        use_case.execute(DeleteRole.Input(id=role.id))

        mock_repository.delete.assert_called_once_with(role.id)

    def test_when_link_not_found_then_raise_exception(self):
        mock_repository = create_autospec(RoleRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteRole(mock_repository)

        with pytest.raises(RoleNotFound):
            use_case.execute(DeleteRole.Input(id=uuid4()))
        
        mock_repository.delete.assert_not_called() 
        assert mock_repository.delete.called is False