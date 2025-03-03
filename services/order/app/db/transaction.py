from contextlib import contextmanager
from sqlalchemy.orm import Session
from typing import Generator
import logging

logger = logging.getLogger(__name__)

@contextmanager
def transaction(db: Session) -> Generator[Session, None, None]:
    try:
        yield db
    except Exception as e:
        logger.error(f"Transaction failed: {str(e)}")
        db.rollback()
        raise
    finally:
        try:
            db.commit()
        except Exception as e:
            logger.error(f"Failed to commit transaction: {str(e)}")
            db.rollback()
            raise 