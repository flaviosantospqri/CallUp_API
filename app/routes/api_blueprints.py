#from app.routes.provider_route import bp_provider
from app.routes.subcategory_route import bp as bp_sub_category
from app.routes.category_route import bp as bp_category
#from app.routes.company_route import bp_company
#from app.routes.call_route import bp_call
from app.routes.sector_route import bp as bp_route
from flask import Blueprint

bp_api = Blueprint("bp_api", __name__, url_prefix="/api")

bp_api.register_blueprint(bp_category)
bp_api.register_blueprint(bp_sub_category)
bp_api.register_blueprint(bp_route)
#bp_api.register_blueprint(bp_call)
#bp_api.register_blueprint(bp_provider)
#bp_api.register_blueprint(bp_company)
