from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.user.repository import SQLAlchemyUserRepository
from src.api.user.schemas import CreateUserInputSchema, CreateUserOutputSchema, ListUserOutputSchema, UpdateUserInputSchema
from src.core.user.application.use_cases.create_user import CreateUser
from src.core.user.application.use_cases.list_user import ListUser
from src.core.user.application.use_cases.delete_user import DeleteUser
from src.core.user.application.use_cases.update_user import UpdateUser
from src.api.database import SessionLocal
from uuid import UUID
from src.core.user.application.use_cases.exceptions import InvalidUserData, UserNotFound
from sqlalchemy.orm import Session

# Criação do blueprint
bp = Blueprint('users', __name__, url_prefix='/users')

# Instância do repositório
session: Session = SessionLocal()
user_repository = SQLAlchemyUserRepository(session)


@bp.route('/', methods=['POST'])
def create_user():
    """
    Cria uma nova user utilizando o caso de uso CreateUser.
    """
    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = CreateUserInputSchema().load(data)
    except InvalidUserData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Executa o caso de uso
    print(validated_input['role_id'])
    print(type(validated_input['role_id']))

    input = CreateUser.Input(name=validated_input['name'], email=validated_input['email'], role_id=validated_input['role_id'], password=validated_input['password'])
    use_case = CreateUser(repository=user_repository)
    try:
        result = use_case.execute(input=input)
    except InvalidUserData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

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


# # @bp.route('/<uuid:user_id>', methods=['GET'])
# # def get_user(user_id):
# #     """
# #     Retorna uma user específica pelo ID.
# #     """
# #     user = user_repository.get_by_id(user_id)
# #     if not user:
# #         return jsonify({'error': 'User não encontrada.'}), HTTPStatus.NOT_FOUND

# #     return jsonify({'id': user.id, 'description': user.description}), HTTPStatus.OK


@bp.route('/<uuid:user_id>', methods=['PATCH'])
def update_user(user_id: UUID):
    """
    Atualiza uma user pelo ID.
    """

    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = UpdateUserInputSchema().load(data)
    except InvalidUserData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
    use_case = UpdateUser(repository=user_repository)
    try:
        use_case.execute(input=UpdateUser.Input(id=user_id, email=validated_input['email'], password=validated_input['password']))
    except UserNotFound as e:
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