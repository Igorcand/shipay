import pytest
from uuid import uuid4
from flask import Flask
from unittest.mock import MagicMock, patch
from src.api.claim.controller import bp
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound

@pytest.fixture
def client():
    """Fixture para configurar o cliente de teste do Flask."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(bp)
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_session():
    """Fixture para criar um mock da sessão do banco de dados."""
    with patch('src.api.claim.controller.SessionLocal', return_value=MagicMock()) as mock_db:
        yield mock_db()

def test_create_claim_success(client, mock_session):
    """Testa a rota POST /claims para criar uma nova claim com sucesso."""
    mock_session.commit = MagicMock()  # Simula o commit do banco

    # Simula o comportamento do caso de uso CreateClaim
    with patch('src.api.claim.controller.CreateClaim') as mock_create_claim:
        mock_create_claim.return_value.execute.return_value = MagicMock(
            id=uuid4(),
            description='Test Claim',
            active=True
        )

        payload = {'description': 'Test Claim', 'active': True}
        response = client.post('/claims/', json=payload)
        assert response.status_code == 201

def test_create_claim_invalid_data(client):
    """Testa a rota POST /claims com dados inválidos."""
    payload = {'invalid_field': 'Test'}
    response = client.post('/claims/', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_list_claims_success(client, mock_session):
    """Testa a rota GET /claims para listar claims."""
    # Simula o comportamento do caso de uso ListClaim
    with patch('src.api.claim.controller.ListClaim') as mock_list_claim:
        mock_list_claim.return_value.execute.return_value = MagicMock(
            data=[
                {'id': str(uuid4()), 'description': 'Claim 1', 'active': True},
                {'id': str(uuid4()), 'description': 'Claim 2', 'active': False}
            ]
        )

        response = client.get('/claims/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data['data'], list)

def test_get_claim_success(client):
    """
    Testa a rota GET /<uuid:claim_id> com um ID válido.
    """
    claim_id = str(uuid4())
    mock_claim = {"id": claim_id, "description": "Test Claim", "active": True}

    with patch("src.api.claim.controller.GetClaim") as mock_use_case:
        mock_use_case.return_value.execute.return_value = mock_claim

        response = client.get(f"/claims/{claim_id}")
        assert response.status_code == 200
        assert response.json == mock_claim

def test_get_claim_not_found(client):
    """
    Testa a rota GET /<uuid:claim_id> com um ID inexistente.
    """
    claim_id = str(uuid4())

    with patch("src.api.claim.controller.GetClaim") as mock_use_case:
        mock_use_case.return_value.execute.side_effect = ClaimNotFound("Claim not found")

        response = client.get(f"/claims/{claim_id}")
        assert response.status_code == 404
        assert response.json == {"error": "Claim not found"}
        
def test_update_claim_success(client, mock_session):
    """Testa a rota PATCH /claims/<claim_id> para atualizar uma claim."""
    claim_id = str(uuid4())
    payload = {'description': 'Updated Claim', 'active': False}

    # Simula o comportamento do caso de uso UpdateClaim
    with patch('src.api.claim.controller.UpdateClaim') as mock_update_claim:
        mock_update_claim.return_value.execute = MagicMock()

        response = client.patch(f'/claims/{claim_id}', json=payload)
        assert response.status_code == 204

def test_update_claim_not_found(client, mock_session):
    """Testa a rota PATCH /claims/<claim_id> quando a claim não é encontrada."""
    claim_id = str(uuid4())
    payload = {'description': 'Updated Claim', 'active': False}

    # Simula o comportamento do caso de uso UpdateClaim
    with patch('src.api.claim.controller.UpdateClaim') as mock_update_claim:
        mock_update_claim.return_value.execute.side_effect = ClaimNotFound("Claim not found")

        response = client.patch(f'/claims/{claim_id}', json=payload)
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Claim not found'

def test_delete_claim_success(client, mock_session):
    """Testa a rota DELETE /claims/<claim_id> para excluir uma claim."""
    claim_id = str(uuid4())

    # Simula o comportamento do caso de uso DeleteClaim
    with patch('src.api.claim.controller.DeleteClaim') as mock_delete_claim:
        mock_delete_claim.return_value.execute = MagicMock()

        response = client.delete(f'/claims/{claim_id}')
        assert response.status_code == 204

def test_delete_claim_not_found(client, mock_session):
    """Testa a rota DELETE /claims/<claim_id> quando a claim não é encontrada."""
    claim_id = str(uuid4())

    # Simula o comportamento do caso de uso DeleteClaim
    with patch('src.api.claim.controller.DeleteClaim') as mock_delete_claim:
        mock_delete_claim.return_value.execute.side_effect = ClaimNotFound("Claim not found")

        response = client.delete(f'/claims/{claim_id}')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Claim not found'