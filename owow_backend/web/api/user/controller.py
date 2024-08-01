import secrets
from typing import Annotated

import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials

from owow_backend.core import logger
from owow_backend.db.dao.user_dao import UserDAO
from owow_backend.db.models import UserDocument
from owow_backend.web.api.file.views import security


class UserController:
    @staticmethod
    async def create_user(username: str, password: str) -> UserDocument:
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(),
        )
        return await UserDAO.create_user(username, hashed_password)

    @staticmethod
    async def get_user(username: str) -> UserDocument:
        user = await UserDAO.get_user(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="UserDocument not found")
        return user

    @staticmethod
    async def verify_password(plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8"),
        )

    @classmethod
    async def authenticate_user(cls, credentials: Annotated[HTTPBasicCredentials, Depends(security)]) -> str:
        user = await cls.get_user(credentials.username)
        is_correct_username = secrets.compare_digest(credentials.username.encode("utf8"), user.username.encode("utf8"))
        is_correct_password = await cls.verify_password(credentials.password, user.hashed_password)

        if not (is_correct_username and is_correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )
        return credentials.username

    @classmethod
    async def create_default_user(cls) -> None:
        default_username = "admin"
        default_password = "adminpassword"

        if not await UserDAO.user_exists(default_username):
            await cls.create_user(default_username, default_password)
            logger.info(f"Default user '{default_username}' created.")
        else:
            logger.info(f"Default user '{default_username}' already exists.")
