from flask import Blueprint
from app.controllers.provider_controller import get_provider_by_cnpj, get_providers, patch_provider

bp = Blueprint('provider', __name__, url_prefix='/provider')

bp.get('')(get_providers)
bp.get('/<str:provider_cnpj>')(get_provider_by_cnpj)
bp.patch('/<str:provider_cnpj>')(patch_provider)