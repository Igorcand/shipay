from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.user.repository import SQLAlchemyUserRepository
from src.api.role.repository import SQLAlchemyRoleRepository

from src.api.user.schemas import CreateUserInputSchema, CreateUserOutputSchema, ListUserOutputSchema, UpdateUserInputSchema, GetUserOutputSchema
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.list_user import ListUser
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.application.use_cases.update_user import UpdateUser
from src.core.user.application.use_cases.get_user import GetUser

from src.api.database import SessionLocal
from uuid import UUID
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound, RelatedRolesNotFound
from sqlalchemy.orm import Session

# Criação do blueprint
bp = Blueprint('users', __name__, url_prefix='/users')

# Instância do repositório
session: Session = SessionLocal()
user_repository = SQLAlchemyUserRepository(session)
role_repository = SQLAlchemyRoleRepository(session)


@bp.route('/', methods=['POST'])
def create_user():
    """
    Cria uma nova user utilizando o caso de uso CreateUser.
    """
    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = CreateUserInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Executa o caso de uso

    input = CreateUser.Input(name=validated_input['name'], email=validated_input['email'], role_id=validated_input['role_id'], password=validated_input['password'])
    use_case = CreateUser(repository=user_repository, role_repository=role_repository)
    try:
        result = use_case.execute(input=input)
    except InvalidUserData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    except RelatedRolesNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da nova user
    output_data = CreateUserOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


@bp.route('/', methods=['GET'])
def list_users():
    """
    Lista todas as users.
    """
    # Executa o caso de uso

    use_case = ListUser(repository=user_repository)
    try:
        result = use_case.execute(input=ListUser.Input())
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Retorna a resposta com o id da nova user
    output_data = ListUserOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


@bp.route('/<uuid:user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retorna uma role específica pelo ID.
    """
    use_case = GetUser(repository=user_repository, role_repository=role_repository)
    try:
        result = use_case.execute(input=GetUser.Input(id=user_id))
    except UserNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    
    output_data = GetUserOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:user_id>', methods=['PATCH'])
def update_user(user_id: UUID):
    """
    Atualiza uma user pelo ID.
    """

    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = UpdateUserInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
    use_case = UpdateUser(repository=user_repository, role_repository=role_repository)
    try:
        use_case.execute(input=UpdateUser.Input(id=user_id, email=validated_input['email'], password=validated_input['password']))
    except UserNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    except RelatedRolesNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da user
    return "", HTTPStatus.NO_CONTENT


@bp.route('/<uuid:user_id>', methods=['DELETE'])
def delete_user(user_id: UUID):
    """
    Exclui uma user pelo ID.
    """
    use_case = DeleteUser(repository=user_repository)
    try:
        use_case.execute(input=DeleteUser.Input(id=user_id))
    except UserNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

   # Retorna a resposta com o id da user
    return "", HTTPStatus.NO_CONTENT