from fastapi import HTTPException
from routers.schemas import PostBase
from database.db_models import DbArticle
from sqlalchemy.orm.session import Session
import datetime


def create_article(db: Session, request: PostBase):
	"""Writes an article in the DB
	"""
	new_article = DbArticle(
		timestamp=datetime.datetime.now(),
		**request.dict()
	)

	db.add(new_article)
	db.commit()
	db.refresh(new_article)  # Adds id to the record

	return new_article


def get_article_list(db: Session):
	return db.query(DbArticle).all()


def delete_article(id: int, db: Session):
	article = db.query(DbArticle).filter(DbArticle.id == id).first()

	if not article:
		raise HTTPException(
			status_code=400,
			detail=f'Post with id {id} does not exist.'
		)

	db.delete(article)
	db.commit()

	return 'OK.'