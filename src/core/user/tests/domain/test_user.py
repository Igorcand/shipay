import pytest
from uuid import uuid4
from src.core.user.domain.user import User

@pytest.mark.user
class TestUser:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            User()

    def test_create_user_with_provided_values(self):
        id = uuid4()
        role_id = uuid4()

        user = User(
            id=id, 
            name="John",
            email="dev@email.com",
            role_id=role_id
            )
        
        assert user.id == id
        assert user.name == "John"
        assert user.email == "dev@email.com"
        assert user.role_id == role_id


