from fastapi import Depends, status
from utils.auth_helper import decode_token
from fastapi.security import OAuth2PasswordBearer
from db.database import get_session
from sqlmodel import Session, select
from db.models import User, LoginSession
from utils.procedures import CustomError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='apps/auth/login')


def get_current_user_dependency(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    try:
        payload = decode_token(token)
        user_id = payload.get('user_id')
        session_id = payload.get('session_id')

        # Single JOIN query instead of two separate SELECTs
        query = select(User, LoginSession).join(
            LoginSession, LoginSession.user_id == User.id
        ).where(User.id == user_id, LoginSession.id == session_id)
        result = db.exec(query).first()

        if not result:
            raise CustomError(status_code=status.HTTP_401_UNAUTHORIZED, message='Invalid_Token')

        user, login_session = result

        if login_session.is_logged_out is True:
            raise CustomError(status_code=status.HTTP_401_UNAUTHORIZED, message='Invalid_Token')

        if user.is_blocked is True:
            raise CustomError(status_code=status.HTTP_403_FORBIDDEN, message='You_Are_Blocked')

        return user

    except CustomError:
        raise
    except Exception:
        raise CustomError(status_code=status.HTTP_401_UNAUTHORIZED, message='Invalid_Token')

