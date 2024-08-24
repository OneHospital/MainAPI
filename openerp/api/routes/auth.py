from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from loguru import logger
from pydantic import HttpUrl
from requests_oauthlib import OAuth2Session
from starlette.requests import Request
from starlette.responses import Response

from openerp.api.operations.user import UserOps
from openerp.api.utilities.token import TokenUtil
from openerp.config import Config
from openerp.exceptions.token import InvalidTokenException

token_util = TokenUtil()

router = APIRouter()


# Endpoint to initiate Google OAuth login
@router.get("/google/login")
async def google_login(state_uri: HttpUrl = None):
    if state_uri:
        state_uri = f'state_uri:{state_uri}'
    google = OAuth2Session(Config.GOOGLE_CLIENT_ID, redirect_uri=Config.GOOGLE_REDIRECT_URI, scope=Config.SCOPE)
    authorization_url, state = google.authorization_url(
        Config.AUTHORIZATION_BASE_URL, access_type="offline", state=state_uri
    )

    return RedirectResponse(authorization_url)


# Endpoint to handle Google OAuth callback
@router.get("/google/callback")
async def google_callback(code: str, state: str, res: Response):
    user_ops = UserOps()
    google = OAuth2Session(Config.GOOGLE_CLIENT_ID, redirect_uri=Config.GOOGLE_REDIRECT_URI)

    # Fetch the access token from Google
    token = google.fetch_token(Config.TOKEN_URL, client_secret=Config.GOOGLE_CLIENT_SECRET, code=code)

    # Use the access token to fetch the user's profile information
    response = google.get(Config.USER_INFO_URL)
    user_info = response.json()

    # Check if user exists in MongoDB
    user = await user_ops.find_user_by_email(user_info["email"])
    if not user:
        # If the user doesn't exist, create a new record
        logger.debug(f"Creating new user with email: {user_info['email']}")
        user_id = await user_ops.create_user({
            "email": user_info["email"],
            "first_name": user_info["given_name"],
            "last_name": user_info["family_name"],
            "google_id": user_info["id"],
            "profile_pic": user_info["picture"],
            "google_token": token
        })
    else:
        # If the user exists, update the user data
        logger.debug(f"Updating user with email: {user_info['email']}")
        user_id = await user_ops.update_user(user_info["email"], {
            "google_id": user_info["id"],
            "profile_pic": user_info["picture"],
            "google_token": token
        })

    # Create access and refresh tokens for the user
    access_token, refresh_token = await token_util.create_token(user_id=user_id)

    if state.startswith("state_uri:"):
        state = state.replace("state_uri:", "")
        res = RedirectResponse(state, status_code=302)

    res.set_cookie(key="access_token", value=access_token, httponly=True)
    expiry_days = Config.REFRESH_TOKEN_EXPIRE_DAYS
    res.set_cookie(key="refresh_token", value=refresh_token, httponly=True, max_age=expiry_days * 24 * 60 * 60)

    return res


# Endpoint to refresh the access token from cookie
@router.post("/token/refresh")
async def refresh_access_token(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise InvalidTokenException("Trying to refresh an access token without refresh token")

    access_token = await token_util.refresh_access_token(refresh_token)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return {"details": "Token refreshed successfully"}
