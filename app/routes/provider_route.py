from flask import Blueprint
from app.controllers.provider_controller import delete_provider, get_provider_by_cnpj, get_providers, patch_provider

bp = Blueprint('provider', __name__, url_prefix='/provider')

bp.get('')(get_providers)
bp.get('/<strring:provider_cnpj>')(get_provider_by_cnpj)
bp.patch('/<string:provider_cnpj>')(patch_provider)
bp.patch('/<provider_id>')(delete_provider)