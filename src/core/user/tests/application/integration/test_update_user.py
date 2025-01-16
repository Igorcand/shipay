from unittest.mock import MagicMock
from uuid import UUID, uuid4
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound, RelatedRolesNotFound
from src.core.user.domain.user_repository import UserRepository
from src.core.user.domain.user import User
from src.core.role.domain.role import Role
import pytest

from src.core.user.infra.in_memory_user_repository import InMemoryUserRepository
from src.core.role.infra.in_memory_role_repository import InMemoryRoleRepository

@pytest.mark.user
class TestUpdateUser:
    def test_update_user_from_repository(self):
        role1 = Role(description="Dev")
        role2 = Role(description="Admin")

        role_repository = InMemoryRoleRepository(roles=[role1, role2])

        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=role1.id
            )

        repository = InMemoryUserRepository(users=[user])

        use_case = UpdateUser(repository=repository, role_repository=role_repository)

        use_case.execute(UpdateUser.Input(id=user.id, email="developer@email.com", password="123", role_id=role2.id))

        updated_user = repository.get_by_id(user.id)
        assert updated_user.id == user.id
        assert updated_user.email == "developer@email.com"
        assert updated_user.password == "123"
        assert updated_user.role_id == role2.id



    def test_update_user_when_user_not_found_then_raise_exception(self):

        repository = InMemoryUserRepository()
        role_repository = InMemoryRoleRepository()

        use_case = UpdateUser(repository=repository, role_repository=role_repository)

        with pytest.raises(UserNotFound):
            use_case.execute(UpdateUser.Input(id=uuid4(), email="developer@email.com"))
    
    def test_update_user_when_related_role_not_found_then_raise_exception(self):

        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=uuid4()
            )

        repository = InMemoryUserRepository(users=[user])
        role_repository = InMemoryRoleRepository()


        use_case = UpdateUser(repository=repository, role_repository=role_repository)

        with pytest.raises(RelatedRolesNotFound):
            use_case.execute(input=UpdateUser.Input(id=user.id, email="developer@email.com", role_id=uuid4()))
        