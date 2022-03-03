from app.routes.provider_services_blueprints import bp_provider_services
from app.routes.sub_categories_blueprints import bp_sub_categories
from app.routes.categories_blueprints import bp_categories
from app.routes.company_blueprints import bp_company
from app.routes.called_blueprints import bp_called
from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

bp_api.register_blueprint(bp_categories)
bp_api.register_blueprint(bp_called)
bp_api.register_blueprint(bp_sub_categories)
bp_api.register_blueprint(bp_provider_services)
bp_api.register_blueprint(bp_company)