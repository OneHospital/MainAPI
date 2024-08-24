from dataclasses import dataclass
from os import path
from decouple import config

# Get the path to the root
_FILE_ROOT_PATH = path.dirname(path.dirname(path.abspath(__file__)))


@dataclass
class Config:
    ROOT_PATH: str = _FILE_ROOT_PATH
    PLUGINS_PATH: str = path.join(ROOT_PATH, "plugins")
    PLUGINS_LIST: str = path.join(PLUGINS_PATH, ".plugins")

    # MongoDB settings
    MONGO_URI = config("MONGO_URI", default="mongodb://localhost:27017")

    # JWT settings
    SECRET_KEY = config("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", default=30, cast=int)
    REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", default=60, cast=int)

    # Google OAuth2 settings
    GOOGLE_CLIENT_ID = config("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = config("GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = config("GOOGLE_REDIRECT_URI", default="http://127.0.0.1:8000/auth/google/callback")
    AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/auth"
    TOKEN_URL = "https://accounts.google.com/o/oauth2/token"
    SCOPE = [
        "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"
    ]
    USER_INFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"
