from fastapi import APIRouter
from app.controllers import defaults_controller

defaults_router = APIRouter(tags=["defaults"])

defaults_router.get("/")(defaults_controller.get_root)
defaults_router.get("/health")(defaults_controller.get_health)
defaults_router.get("/ping")(defaults_controller.get_ping)
