from database import database_config
from domain import models

def insertFestival(festival:models.Festival):
    db = database_config.SessionLocal()
    try:
        db.add(festival)
        db.commit()
        db.refresh(festival)
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def existFestivalByTitle(title: str) -> bool:
    db = database_config.SessionLocal()
    try:
        festival = db.query(models.Festival).filter(models.Festival.title == title).first()
        return festival is not None
    finally:
        db.close()