from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.user.repository import SQLAlchemyUserRepository
from src.api.role.repository import SQLAlchemyRoleRepository
from src.api.claim.repository import SQLAlchemyClaimRepository

from src.api.user.schemas import (
    CreateUserInputSchema,
    CreateUserOutputSchema,
    ListUserOutputSchema,
    UpdateUserInputSchema,
    UserOutputSchema
)
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.list_user import ListUser
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.get_user import GetUser
from src.api.database import SessionLocal
from uuid import UUID
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from sqlalchemy.orm import Session
from flasgger import Swagger

# Criação do blueprint
bp = Blueprint('users', __name__, url_prefix='/users')

# Instância do repositório
session: Session = SessionLocal()
user_repository = SQLAlchemyUserRepository(session)
role_repository = SQLAlchemyRoleRepository(session)
claim_repository = SQLAlchemyClaimRepository(session)

# Inicializando o Swagger
swagger = Swagger()

@bp.route('/', methods=['POST'])
def create_user():
    """
    Cria um novo usuário utilizando o caso de uso CreateUser.
    ---
    tags:
      - Users
    parameters:
      - name: name
        in: body
        required: true
        type: string
        description: Nome do usuário
      - name: email
        in: body
        required: true
        type: string
        description: E-mail do usuário
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          id: CreateUserOutputSchema
      400:
        description: Dados inválidos
    """
    data = request.get_json()
    try:
        validated_input = CreateUserInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    input = CreateUser.Input(name=validated_input['name'], email=validated_input['email'], role_id=validated_input["role_id"], claim_ids=set(validated_input["claim_ids"]))
    use_case = CreateUser(repository=user_repository, role_repository=role_repository, claim_repository=claim_repository)
    try:
        result = use_case.execute(input=input)
    except InvalidUserData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    output_data = CreateUserOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


@bp.route('/', methods=['GET'])
def list_users():
    """
    Lista todos os usuários.
    ---
    tags:
      - Users
    responses:
      200:
        description: Lista de todos os usuários
        schema:
          id: ListUserOutputSchema
      400:
        description: Erro ao listar usuários
    """
    use_case = ListUser(repository=user_repository, role_repository=role_repository, claim_repository=claim_repository)
    try:
        result = use_case.execute(input=ListUser.Input())
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    output_data = ListUserOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retorna um usuário específico pelo ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        required: true
        type: string
        description: ID do usuário a ser retornado
    responses:
      200:
        description: Dados do usuário encontrado
        schema:
          id: UserOutputSchema
      404:
        description: Usuário não encontrado
    """
    use_case = GetUser(repository=user_repository, role_repository=role_repository, claim_repository=claim_repository)
    try:
        result = use_case.execute(input=GetUser.Input(id=user_id))
    except UserNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    output_data = UserOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:user_id>', methods=['PATCH'])
def update_user(user_id: UUID):
    """
    Atualiza um usuário pelo ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        required: true
        type: string
        description: ID do usuário a ser atualizado
      - name: name
        in: body
        required: true
        type: string
        description: Novo nome do usuário
      - name: email
        in: body
        required: true
        type: string
        description: Novo e-mail do usuário
    responses:
      204:
        description: Usuário atualizado com sucesso
      400:
        description: Dados inválidos
      404:
        description: Usuário não encontrado
    """
    data = request.get_json()
    try:
        validated_input = UpdateUserInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    use_case = UpdateUser(repository=user_repository, role_repository=role_repository, claim_repository=claim_repository)
    try:
        use_case.execute(input=UpdateUser.Input(id=user_id, password=validated_input['password'], email=validated_input['email'], role_id=validated_input["role_id"]))
    except UserNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT


@bp.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id: UUID):
    """
    Exclui um usuário pelo ID.
    ---
    tags:
      - Users
    parameters:
      - name: user_id
        in: path
        required: true
        type: string
        description: ID do usuário a ser excluído
    responses:
      204:
        description: Usuário excluído com sucesso
      404:
        description: Usuário não encontrado
    """
    use_case = DeleteUser(repository=user_repository)
    try:
        use_case.execute(input=DeleteUser.Input(id=user_id))
    except UserNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT
