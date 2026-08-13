from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union

from app.core.security.auth_handler import AuthHandler
from app.services.user_service import UserService
from app.db.database import get_session 
from app.schemas.user_schema import UserPublic

AUTH_PREFIX = 'Bearer '

def get_current_user(
    session : Session = Depends(get_session), 
    authorization : Annotated[Union[str, None], Header()] = None
) -> UserPublic : 
    # Custom exception
    auth_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Authentication Credentials"
    )

    if not authorization: 
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX): 
        raise auth_exception

    payload = AuthHandler.decode_jwt(token=authorization[len(AUTH_PREFIX):])

    if payload and payload["user_email"] : 
        try: 
            user = UserService(session=session).get_user_by_email(payload["user_email"])

            return UserPublic(
                email=user.email,
                name=user.name
            )
        except Exception as error: 
            raise error

    raise auth_exception