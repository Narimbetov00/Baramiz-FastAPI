from fastapi.security import HTTPBearer
from fastapi import Request, Depends
from .utils import decode_token
from fastapi.exceptions import HTTPException
from typing import Any
from src.db.models import User

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        creds = await super().__call__(request)
        token = creds.credentials
        token_data = decode_token(token)

        if not self.token_valid(token): 
            raise HTTPException(status_code=403,detail="Invalid or expired token")

        # if await token_in_blocklist(token_data['jti']):
        #     raise InvalidToken()

        if token_data["refresh"]:
            raise HTTPException(
                status_code=403, detail="Please provide an access token"
            )

        self.verify_token_data(token_data)

        return token_data

    def token_valid(self, token: str) -> bool:
        token_data = decode_token(token)
        return token_data is not None

    def verify_token_data(self, token_data):
        raise NotImplementedError("Please override this method in child classes")

class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=403,detail="Please provide a valid access token")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=403,detail="Please provide a valid refresh token")

async def get_current_user(token_details: dict = Depends(AccessTokenBearer())):

    user_username = token_details['user']['username']

    user = await User.get_or_none(username=user_username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

class RoleChecker:
    def __init__(self, allowed_roles: list[str]) -> None:
        self.allowed_roles = allowed_roles

    async def __call__(self, current_user: User = Depends(get_current_user)) -> Any:
        if not current_user.is_verified:
            raise HTTPException(status_code=404,detail="User Not Found")

        if current_user.role in self.allowed_roles:
            return True

        raise HTTPException(status_code=500,detail="Oops! ... Something went wrong")
