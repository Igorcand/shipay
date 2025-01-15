from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.role.application.use_cases.update_role import UpdateRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from src.core.role.domain.role_repository import RoleRepository
from src.core.role.domain.role import Role
from unittest.mock import create_autospec
import pytest



@pytest.mark.role
class TestDeleteRole:
    def test_update_role_from_repository(self):
        id = uuid4()
        role = Role(
            description="Developer", 
            id=id, 
            )

        mock_repository = create_autospec(RoleRepository)
        mock_repository.get_by_id.return_value = role

        use_case = UpdateRole(repository=mock_repository)
        use_case.execute(UpdateRole.Input(id=id, description="Developer Sr"))

        mock_repository.update.assert_called_once_with(role)

    def test_update_role_when_role_not_found_then_raise_exception(self):

        mock_repository = create_autospec(RoleRepository)
        mock_repository.get_by_id.return_value = None

        use_case = UpdateRole(repository=mock_repository)

        with pytest.raises(RoleNotFound):
            use_case.execute(UpdateRole.Input(id=uuid4(), description="Developer Sr"))
        
        mock_repository.update.assert_not_called() 
        assert mock_repository.update.called is False