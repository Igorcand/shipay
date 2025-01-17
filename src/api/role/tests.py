import pytest
from uuid import uuid4, UUID
from flask import Flask
from src.api.role.controller import bp
from src.api.database import SessionLocal
from unittest.mock import MagicMock, patch
from src.core.role.application.use_cases.exceptions import RoleNotFound

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
    with patch('src.api.role.controller.SessionLocal', return_value=MagicMock()) as mock_db:
        yield mock_db()

def test_create_role_success(client, mock_session):
    """Testa a rota POST /roles para criar uma nova role com sucesso."""
    mock_session.commit = MagicMock()  # Simula o commit do banco

    # Simula o comportamento do caso de uso CreateRole
    with patch('src.api.role.controller.CreateRole') as mock_create_role:
        mock_create_role.return_value.execute.return_value = MagicMock(
            id=uuid4(),
            description='Test Role'
        )

        payload = {'description': 'Test Role'}
        response = client.post('/roles/', json=payload)
        assert response.status_code == 201
        data = response.get_json()

def test_create_role_invalid_data(client):
    """Testa a rota POST /roles com dados inválidos."""
    payload = {'invalid_field': 'Test'}
    response = client.post('/roles/', json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_list_roles_empty(client, mock_session):
    """Testa a rota GET /roles para listar roles."""
    # Simula o comportamento do caso de uso ListRole
    with patch('src.api.role.controller.ListRole') as mock_list_role:
        mock_list_role.return_value.execute.return_value = MagicMock(
            data=[]
        )

        response = client.get('/roles/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data['data'], list)
        assert len(data['data']) == 0

def test_list_roles_success(client, mock_session):
    """Testa a rota GET /roles para listar roles."""
    # Simula o comportamento do caso de uso ListRole
    with patch('src.api.role.controller.ListRole') as mock_list_role:
        mock_list_role.return_value.execute.return_value = MagicMock(
            data=[
                {'id': uuid4(), 'description': 'Role 1'},
                {'id': uuid4(), 'description': 'Role 2'}
            ]
        )

        response = client.get('/roles/')
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data['data'], list)

def test_get_role_success(client):
    """
    Testa a rota GET /<uuid:role_id> com um ID válido.
    """
    role_id = str(uuid4())
    mock_role = {"id": role_id, "description": "Admin"}

    with patch("src.api.role.controller.GetRole") as mock_use_case:
        mock_use_case.return_value.execute.return_value = mock_role

        response = client.get(f"/roles/{role_id}")
        assert response.status_code == 200
        assert response.json == mock_role

def test_get_role_not_found(client):
    """
    Testa a rota GET /<uuid:role_id> com um ID inexistente.
    """
    role_id = str(uuid4())

    with patch("src.api.role.controller.GetRole") as mock_use_case:
        mock_use_case.return_value.execute.side_effect = RoleNotFound("Role not found")

        response = client.get(f"/roles/{role_id}")
        assert response.status_code == 404
        assert response.json == {"error": "Role not found"}

def test_update_role_success(client, mock_session):
    """Testa a rota PATCH /roles/<role_id> para atualizar uma role."""
    role_id = str(uuid4())
    payload = {'description': 'Updated Role'}
    
    # Simula o comportamento do caso de uso UpdateRole
    with patch('src.api.role.controller.UpdateRole') as mock_update_role:
        mock_update_role.return_value.execute = MagicMock()

        response = client.patch(f'/roles/{role_id}', json=payload)
        assert response.status_code == 204

def test_update_role_not_found(client, mock_session):
    """Testa a rota PATCH /roles/<role_id> quando a role não é encontrada."""
    role_id = str(uuid4())
    payload = {'description': 'Updated Role'}
    
    # Simula o comportamento do caso de uso UpdateRole
    with patch('src.api.role.controller.UpdateRole') as mock_update_role:
        mock_update_role.return_value.execute.side_effect = RoleNotFound("Role not found")

        response = client.patch(f'/roles/{role_id}', json=payload)
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Role not found'

def test_delete_role_success(client, mock_session):
    """Testa a rota DELETE /roles/<role_id> para excluir uma role."""
    role_id = str(uuid4())
    
    # Simula o comportamento do caso de uso DeleteRole
    with patch('src.api.role.controller.DeleteRole') as mock_delete_role:
        mock_delete_role.return_value.execute = MagicMock()

        response = client.delete(f'/roles/{role_id}')
        assert response.status_code == 204

def test_delete_role_not_found(client, mock_session):
    """Testa a rota DELETE /roles/<role_id> quando a role não é encontrada."""
    role_id = str(uuid4())
    
    # Simula o comportamento do caso de uso DeleteRole
    with patch('src.api.role.controller.DeleteRole') as mock_delete_role:
        mock_delete_role.return_value.execute.side_effect = RoleNotFound("Role not found")

        response = client.delete(f'/roles/{role_id}')
        assert response.status_code == 404
        data = response.get_json()
        assert data['error'] == 'Role not found'
