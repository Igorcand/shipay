from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.role.repository import SQLAlchemyRoleRepository
from src.api.role.schemas import CreateRoleInputSchema, CreateRoleOutputSchema, ListRoleOutputSchema, UpdateRoleInputSchema
from src.core.role.application.use_cases.create_role import CreateRole
from src.core.role.application.use_cases.list_role import ListRole
from src.core.role.application.use_cases.delete_role import DeleteRole
from src.core.role.application.use_cases.update_role import UpdateRole
from src.api.database import SessionLocal
from uuid import UUID
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from sqlalchemy.orm import Session

# Criação do blueprint
bp = Blueprint('roles', __name__, url_prefix='/roles')

# Instância do repositório
session: Session = SessionLocal()
role_repository = SQLAlchemyRoleRepository(session)


@bp.route('/', methods=['POST'])
def create_role():
    """
    Cria uma nova role utilizando o caso de uso CreateRole.
    """
    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = CreateRoleInputSchema().load(data)
    except InvalidRoleData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Executa o caso de uso
    input = CreateRole.Input(description=validated_input['description'])
    use_case = CreateRole(repository=role_repository)
    try:
        result = use_case.execute(input=input)
    except InvalidRoleData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Retorna a resposta com o id da nova role
    output_data = CreateRoleOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


@bp.route('/', methods=['GET'])
def list_roles():
    """
    Lista todas as roles.
    """
    # Executa o caso de uso

    use_case = ListRole(repository=role_repository)
    try:
        result = use_case.execute(input=ListRole.Input())
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Retorna a resposta com o id da nova role
    output_data = ListRoleOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


# @bp.route('/<uuid:role_id>', methods=['GET'])
# def get_role(role_id):
#     """
#     Retorna uma role específica pelo ID.
#     """
#     role = role_repository.get_by_id(role_id)
#     if not role:
#         return jsonify({'error': 'Role não encontrada.'}), HTTPStatus.NOT_FOUND

#     return jsonify({'id': role.id, 'description': role.description}), HTTPStatus.OK


@bp.route('/<uuid:role_id>', methods=['PATCH'])
def update_role(role_id: UUID):
    """
    Atualiza uma role pelo ID.
    """

    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = UpdateRoleInputSchema().load(data)
    except InvalidRoleData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
    use_case = UpdateRole(repository=role_repository)
    try:
        use_case.execute(input=UpdateRole.Input(id=role_id, description=validated_input['description']))
    except RoleNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da role
    return "", HTTPStatus.NO_CONTENT


@bp.route('/<uuid:role_id>', methods=['DELETE'])
def delete_role(role_id: UUID):
    """
    Exclui uma role pelo ID.
    """
    use_case = DeleteRole(repository=role_repository)
    try:
        use_case.execute(input=DeleteRole.Input(id=role_id))
    except RoleNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da role
    return "", HTTPStatus.NO_CONTENT
