from fastapi import APIRouter, Depends
from starlette import status

from src.api.accounts.accounts_response import AccountsResponseSchema
from src.api.accounts.service.accounts_api_service import AccountsApiService
from src.api.dependencies import get_current_user, get_account_api_service
from src.schemas.user_shemas import UserReadSchema
from src.api.accounts.accounts_response import AccountResponseSchema

account_router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)

@account_router.get(
    "/me",
    response_model=AccountsResponseSchema,
    status_code=status.HTTP_200_OK,
)

async def get_me(
        current_user: UserReadSchema = Depends(get_current_user),
        account_api_service: AccountsApiService = Depends(get_account_api_service)
):
    return await account_api_service.get_accounts_by_user_id(current_user.id)