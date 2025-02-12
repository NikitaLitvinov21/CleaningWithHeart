from functools import wraps
from typing import Any, Callable

from sqlalchemy.orm import Session

from database.connector import get_session


def transaction(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session: Session = get_session()
        try:
            result = func(*args, session=session, **kwargs)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    return wrapper
