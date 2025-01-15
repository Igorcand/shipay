import pytest
from uuid import uuid4
from src.core.claim.domain.claim import Claim

@pytest.mark.claim
class TestClaim:
    def test_field_is_required(self):
        with pytest.raises(TypeError):
            Claim()

    def test_description_must_have_be_less_characters(self):
        with pytest.raises(ValueError, match="description cannot be longer than 255"):
            Claim(description='a'*256)

    def test_cannot_create_claim_with_empty_description(self):
        with pytest.raises(ValueError, match="description cannot be empty"):
            Claim(description='')

    def test_create_claim_with_provided_values(self):
        id = uuid4()

        user = Claim(
            id=id, 
            description="Developer",
            active=True
            )
        
        assert user.id == id
        assert user.description == "Developer"
        assert user.active == True
    
    def test_create_claim_with_default_values(self):
        id = uuid4()

        user = Claim(
            id=id, 
            description="Developer"
            )
        
        assert user.id == id
        assert user.description == "Developer"
        assert user.active == False


