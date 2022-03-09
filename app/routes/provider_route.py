from flask import Blueprint
from app.controllers.provider_controller import delete_provider, get_provider_by_cnpj, get_providers, patch_provider, post_login_provider, post_register_provider

bp = Blueprint('provider', __name__, url_prefix='/provider')

bp.get('')(get_providers)
bp.get('/<string:provider_cnpj>')(get_provider_by_cnpj)
bp.patch('/<string:provider_cnpj>')(patch_provider)
bp.post('/register')(post_register_provider)
bp.post('/login')(post_login_provider)
bp.delete('/<provider_id>')(delete_provider)

