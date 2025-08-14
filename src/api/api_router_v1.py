from fastapi import APIRouter
from src.api.auth.routes.auth_route import auth_route
from src.api.users.routes.users_route import users_router
from src.api.accounts.routes.accounts_route import account_router
from src.api.payments.routes.payments_route import payments_router

api_router_v1 = APIRouter(prefix="/api/v1")

api_router_v1.include_router(auth_route)
api_router_v1.include_router(users_router)
api_router_v1.include_router(account_router)
api_router_v1.include_router(payments_router)