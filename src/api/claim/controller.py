from flask import Blueprint, request, jsonify
from http import HTTPStatus
from src.api.claim.repository import SQLAlchemyClaimRepository
from src.api.claim.schemas import CreateClaimInputSchema, CreateClaimOutputSchema, ListClaimOutputSchema, UpdateClaimInputSchema
from src.core.claim.application.use_cases.create_claim import CreateClaim
from src.core.claim.application.use_cases.list_claim import ListClaim
from src.core.claim.application.use_cases.delete_claim import DeleteClaim
from src.core.claim.application.use_cases.update_claim import UpdateClaim
from src.api.database import SessionLocal
from uuid import UUID
from src.core.claim.application.use_cases.exceptions import InvalidClaimData, ClaimNotFound
from sqlalchemy.orm import Session

# Criação do blueprint
bp = Blueprint('claims', __name__, url_prefix='/claims')

# Instância do repositório
session: Session = SessionLocal()
claim_repository = SQLAlchemyClaimRepository(session)


@bp.route('/', methods=['POST'])
def create_claim():
    """
    Cria uma nova claim utilizando o caso de uso CreateClaim.
    """
    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = CreateClaimInputSchema().load(data)
    except InvalidClaimData as e:
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
    """
    # Executa o caso de uso

    use_case = ListClaim(repository=claim_repository)
    try:
        result = use_case.execute(input=ListClaim.Input())
    except Exception as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST

    # Retorna a resposta com o id da nova claim
    output_data = ListClaimOutputSchema().dump(result)
    return jsonify(output_data), HTTPStatus.CREATED


# @bp.route('/<uuid:claim_id>', methods=['GET'])
# def get_claim(claim_id):
#     """
#     Retorna uma claim específica pelo ID.
#     """
#     claim = claim_repository.get_by_id(claim_id)
#     if not claim:
#         return jsonify({'error': 'Claim não encontrada.'}), HTTPStatus.NOT_FOUND

#     return jsonify({'id': claim.id, 'description': claim.description}), HTTPStatus.OK


@bp.route('/<uuid:claim_id>', methods=['PATCH'])
def update_claim(claim_id: UUID):
    """
    Atualiza uma claim pelo ID.
    """

    # Recebe e valida os dados de entrada
    data = request.get_json()
    try:
        validated_input = UpdateClaimInputSchema().load(data)
    except InvalidClaimData as e:
        return jsonify({"error": str(e)}), HTTPStatus.BAD_REQUEST
    
    use_case = UpdateClaim(repository=claim_repository)
    try:
        print(validated_input['active'])
        use_case.execute(input=UpdateClaim.Input(id=claim_id, description=validated_input['description'], active=validated_input['active']))
    except ClaimNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da claim
    return "", HTTPStatus.NO_CONTENT


@bp.route('/<uuid:claim_id>', methods=['DELETE'])
def delete_claim(claim_id: UUID):
    """
    Exclui uma claim pelo ID.
    """
    use_case = DeleteClaim(repository=claim_repository)
    try:
        use_case.execute(input=DeleteClaim.Input(id=claim_id))
    except ClaimNotFound as e:
        return jsonify({"error": str(e)}), HTTPStatus.NOT_FOUND

    # Retorna a resposta com o id da claim
    return "", HTTPStatus.NO_CONTENT
