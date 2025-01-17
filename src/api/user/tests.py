import pytest
from flask import Flask
from unittest.mock import patch
from uuid import uuid4

from src.api.user.controller import bp
from src.core.user.application.use_cases.exceptions import (
    InvalidUserData,
    UserNotFound,
    RelatedRolesNotFound
)


@pytest.fixture
def client():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.testing = True
    return app.test_client()


def test_create_user_success(client):
    """
    Testa a criação de usuário com dados válidos.
    """
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role_id": str(uuid4())
    }

    expected_response = {
        "id": str(uuid4()),
        "name": user_data["name"],
        "email": user_data["email"]
    }

    with patch("src.api.user.controller.CreateUser") as mock_use_case:
        mock_use_case.return_value.execute.return_value = expected_response

        response = client.post("/users/", json=user_data)
        assert response.status_code == 201


def test_create_user_invalid_data(client):
    """
    Testa a criação de usuário com dados inválidos.
    """
    user_data = {
        "name": "John",  # Nome inválido (vazio)
        "email": "invalid_email",  # Email inválido
        "password": "pass",
        "role_id": str(uuid4())
    }

    with patch("src.api.user.controller.CreateUser") as mock_use_case:
        mock_use_case.return_value.execute.side_effect = InvalidUserData("Invalid user data")

        response = client.post("/users/", json=user_data)
        assert response.status_code == 400


def test_list_users_success(client):
    """
    Testa a listagem de usuários.
    """
    mock_users = [
        {"id": str(uuid4()), "name": "User1", "email": "user1@example.com", "role_id": str(uuid4())},
        {"id": str(uuid4()), "name": "User2", "email": "user2@example.com", "role_id": str(uuid4())}
    ]

    with patch("src.api.user.controller.ListUser") as mock_use_case:
        mock_use_case.return_value.execute.return_value = mock_users

        response = client.get("/users/")
        assert response.status_code == 201


def test_update_user_success(client):
    """
    Testa a atualização de um usuário existente.
    """
    user_id = str(uuid4())
    update_data = {"email": "updated@example.com", "password": "newpassword123"}

    with patch("src.api.user.controller.UpdateUser") as mock_use_case:
        mock_use_case.return_value.execute.return_value = None

        response = client.patch(f"/users/{user_id}", json=update_data)
        assert response.status_code == 204


def test_update_user_not_found(client):
    """
    Testa a tentativa de atualizar um usuário inexistente.
    """
    user_id = str(uuid4())
    update_data = {"email": "updated@example.com", "password": "newpassword123"}

    with patch("src.api.user.controller.UpdateUser") as mock_use_case:
        mock_use_case.return_value.execute.side_effect = UserNotFound("User not found")

        response = client.patch(f"/users/{user_id}", json=update_data)
        assert response.status_code == 404
        assert response.json == {"error": "User not found"}


def test_delete_user_success(client):
    """
    Testa a exclusão de um usuário existente.
    """
    user_id = str(uuid4())

    with patch("src.api.user.controller.DeleteUser") as mock_use_case:
        mock_use_case.return_value.execute.return_value = None

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204


def test_delete_user_not_found(client):
    """
    Testa a tentativa de excluir um usuário inexistente.
    """
    user_id = str(uuid4())

    with patch("src.api.user.controller.DeleteUser") as mock_use_case:
        mock_use_case.return_value.execute.side_effect = UserNotFound("User not found")

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 404
        assert response.json == {"error": "User not found"}
