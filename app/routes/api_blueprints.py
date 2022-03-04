from app.routes.provider_blueprints import bp_provider
from app.routes.subcategory_blueprints import bp_sub_category
from app.routes.category_blueprints import bp_category
from app.routes.company_blueprints import bp_company
from app.routes.call_blueprints import bp_call
from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

bp_api.register_blueprint(bp_category)
bp_api.register_blueprint(bp_call)
bp_api.register_blueprint(bp_sub_category)
bp_api.register_blueprint(bp_provider)
bp_api.register_blueprint(bp_company)
