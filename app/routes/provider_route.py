from flask import Blueprint
from app.controllers.provider_controller import (
    delete_provider,
    get_provider_by_id,
    get_providers,
    patch_provider,
    login_provider,
    create_provider,
)

bp = Blueprint("provider", __name__, url_prefix="/providers")

bp.get("")(get_providers)
bp.get("/<provider_id>")(get_provider_by_id)
bp.patch("/<provider_id>")(patch_provider)
bp.post("")(create_provider)
bp.post("/login")(login_provider)
bp.delete("/<provider_id>")(delete_provider)
