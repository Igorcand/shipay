import pytest
from uuid import uuid4
from src.core.role.domain.role import Role

@pytest.mark.role
class TestRole:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            Role()

    def test_description_must_have_be_less_characters(self):
        with pytest.raises(ValueError, match="description cannot be longer than 255"):
            Role(description='a'*256)

    def test_cannot_create_role_with_empty_description(self):
        with pytest.raises(ValueError, match="description cannot be empty"):
            Role(description='')

    def test_create_role_with_provided_values(self):
        id = uuid4()

        user = Role(
            id=id, 
            description="Developer",
            )
        
        assert user.id == id
        assert user.description == "Developer"

