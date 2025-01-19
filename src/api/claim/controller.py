from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.claim.repository import SQLAlchemyClaimRepository
from src.api.claim.schemas import CreateClaimInputSchema, CreateClaimOutputSchema, ListClaimOutputSchema, UpdateClaimInputSchema, ClaimOutputSchema
from src.core.claim.application.use_cases.create_claim import CreateClaim
from src.core.claim.application.use_cases.list_claim import ListClaim
from src.core.claim.application.use_cases.delete_claim import DeleteClaim
from src.core.claim.application.use_cases.update_claim import UpdateClaim
from src.core.claim.application.use_cases.get_claim import GetClaim
from src.api.database import SessionLocal
from uuid import UUID
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from sqlalchemy.orm import Session
from flasgger import Swagger

# Criação do blueprint
bp = Blueprint('claims', __name__, url_prefix='/claims')

# Instância do repositório
session: Session = SessionLocal()
claim_repository = SQLAlchemyClaimRepository(session)

# Inicializando o Swagger
swagger = Swagger()

@bp.route('/', methods=['POST'])
def create_claim():
    """
    Cria uma nova claim utilizando o caso de uso CreateClaim.
    ---
    tags:
      - Claims
    parameters:
      - name: description
        in: body
        required: true
        type: string
        description: Descrição da claim
      - name: active
        in: body
        required: true
        type: boolean
        description: Status ativo da claim
    responses:
      201:
        description: Claim criada com sucesso
        schema:
          id: CreateClaimOutputSchema
      400:
        description: Dados inválidos
    """
    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = CreateClaimInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Executa o caso de uso
    input = CreateClaim.Input(description=validated_input['description'], active=validated_input['active'])
    use_case = CreateClaim(repository=claim_repository)
    try:
        result = use_case.execute(input=input)
    except InvalidClaimData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Retorna a resposta com o id da nova claim
    output_data = CreateClaimOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


@bp.route('/', methods=['GET'])
def list_claims():
    """
    Lista todas as claims.
    ---
    tags:
      - Claims
    responses:
      200:
        description: Lista de todas as claims
        schema:
          id: ListClaimOutputSchema
      400:
        description: Erro ao listar claims
    """
    # Executa o caso de uso

    use_case = ListClaim(repository=claim_repository)
    try:
        result = use_case.execute(input=ListClaim.Input())
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Retorna a resposta com a lista de claims
    output_data = ListClaimOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:claim_id>', methods=['GET'])
def get_claim(claim_id):
    """
    Retorna uma claim específica pelo ID.
    ---
    tags:
      - Claims
    parameters:
      - name: claim_id
        in: path
        required: true
        type: string
        description: ID da claim a ser retornada
    responses:
      200:
        description: Dados da claim encontrada
        schema:
          id: ClaimOutputSchema
      404:
        description: Claim não encontrada
    """
    use_case = GetClaim(repository=claim_repository)
    try:
        result = use_case.execute(input=GetClaim.Input(id=claim_id))
    except ClaimNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND
    
    output_data = ClaimOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.OK


@bp.route('/<uuid:claim_id>', methods=['PATCH'])
def update_claim(claim_id: UUID):
    """
    Atualiza uma claim pelo ID.
    ---
    tags:
      - Claims
    parameters:
      - name: claim_id
        in: path
        required: true
        type: string
        description: ID da claim a ser atualizada
      - name: description
        in: body
        required: true
        type: string
        description: Nova descrição da claim
      - name: active
        in: body
        required: true
        type: boolean
        description: Novo status ativo da claim
    responses:
      204:
        description: Claim atualizada com sucesso
      400:
        description: Dados inválidos
      404:
        description: Claim não encontrada
    """
    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = UpdateClaimInputSchema().load(data)
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
    use_case = UpdateClaim(repository=claim_repository)
    try:
        use_case.execute(input=UpdateClaim.Input(id=claim_id, description=validated_input['description'], active=validated_input['active']))
    except ClaimNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da claim
    return "", HTTPStatus.NO_CONTENT


@bp.route('/<uuid:claim_id>', methods=['DELETE'])
def delete_claim(claim_id: UUID):
    """
    Exclui uma claim pelo ID.
    ---
    tags:
      - Claims
    parameters:
      - name: claim_id
        in: path
        required: true
        type: string
        description: ID da claim a ser excluída
    responses:
      204:
        description: Claim excluída com sucesso
      404:
        description: Claim não encontrada
    """
    use_case = DeleteClaim(repository=claim_repository)
    try:
        use_case.execute(input=DeleteClaim.Input(id=claim_id))
    except ClaimNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da claim
    return "", HTTPStatus.NO_CONTENT
