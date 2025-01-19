from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.role.repository import SQLAlchemyRoleRepository
from src.api.role.schemas import (
    CreateRoleInputSchema,
    CreateRoleOutputSchema,
    ListRoleOutputSchema,
    UpdateRoleInputSchema,
    RoleOutputSchema
)
from src.core.role.application.use_cases.create_role import CreateRole
from src.core.role.application.use_cases.list_role import ListRole
from src.core.role.application.use_cases.delete_role import DeleteRole
from src.core.role.application.use_cases.update_role import UpdateRole
from src.core.role.application.use_cases.get_role import GetRole
from src.core.role.application.use_cases.exceptions import InvalidRoleData, RoleNotFound
from src.api.database import SessionLocal
from sqlalchemy.orm import Session
from uuid import UUID

bp = Blueprint('roles', __name__, url_prefix='/roles')

# Instância do repositório
session: Session = SessionLocal()
role_repository = SQLAlchemyRoleRepository(session)


@bp.route('/', methods=['POST'])
def create_role():
    """
    Cria uma nova role.
    ---
    tags:
      - Roles
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              description:
                type: string
                example: "Administrador"
    responses:
      201:
        description: Role criada com sucesso.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateRoleOutputSchema'
      400:
        description: Dados inválidos.
    """
    data = request.get_json()
    try:
        validated_input = CreateRoleInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    input = CreateRole.Input(description=validated_input['description'])
    use_case = CreateRole(repository=role_repository)
    try:
        result = use_case.execute(input=input)
    except InvalidRoleData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    output_data = CreateRoleOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


@bp.route('/', methods=['GET'])
def list_roles():
    """
    Lista todas as roles.
    ---
    tags:
      - Roles
    responses:
      200:
        description: Lista de roles retornada com sucesso.
        content:
          application/json:
            schema:
              type: array
              items:
                $ref: '#/components/schemas/ListRoleOutputSchema'
      400:
        description: Erro ao listar as roles.
    """
    use_case = ListRole(repository=role_repository)
    try:
        result = use_case.execute(input=ListRole.Input())
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    output_data = ListRoleOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:role_id>', methods=['GET'])
def get_role(role_id):
    """
    Retorna uma role pelo ID.
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        required: true
        schema:
          type: string
          format: uuid
    responses:
      200:
        description: Role retornada com sucesso.
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoleOutputSchema'
      404:
        description: Role não encontrada.
    """
    use_case = GetRole(repository=role_repository)
    try:
        result = use_case.execute(input=GetRole.Input(id=role_id))
    except RoleNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    output_data = RoleOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:role_id>', methods=['PATCH'])
def update_role(role_id: UUID):
    """
    Atualiza uma role pelo ID.
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        required: true
        schema:
          type: string
          format: uuid
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              description:
                type: string
                example: "Administrador Atualizado"
    responses:
      204:
        description: Role atualizada com sucesso.
      400:
        description: Dados inválidos.
      404:
        description: Role não encontrada.
    """
    data = request.get_json()
    try:
        validated_input = UpdateRoleInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    use_case = UpdateRole(repository=role_repository)
    try:
        use_case.execute(input=UpdateRole.Input(id=role_id, description=validated_input['description']))
    except RoleNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT


@bp.route('/<uuid:role_id>', methods=['DELETE'])
def delete_role(role_id: UUID):
    """
    Exclui uma role pelo ID.
    ---
    tags:
      - Roles
    parameters:
      - name: role_id
        in: path
        required: true
        schema:
          type: string
          format: uuid
    responses:
      204:
        description: Role excluída com sucesso.
      404:
        description: Role não encontrada.
    """
    use_case = DeleteRole(repository=role_repository)
    try:
        use_case.execute(input=DeleteRole.Input(id=role_id))
    except RoleNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    return "", HTTPStatus.NO_CONTENT
