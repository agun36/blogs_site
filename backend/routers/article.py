import shutil
import string
import random
from fastapi import APIRouter, Depends
# File, UploadFile
from sqlalchemy.orm import Session
from routers.schemas import PostBase
# form routers.schemas import PostDisplay
from database.db_setup import get_db
from database import db_article


router = APIRouter(
	prefix='/articles',
	tags=['Articles']
)


@router.post('', status_code=201)
def post_article(request: PostBase, db: Session = Depends(get_db)):
	return db_article.create_article(db, request)


@router.get('', status_code=200) )
def get_all(db: Session = Depends(get_db)):
	return db_article.get_article_list(db)


@router.delete('/{id}', status_code=200)
def delete_article(id: int, db:Session = Depends(get_db)):
	return db_article.delete_article(id, db)


# @router.post('/image')
# def upload_image(image: UploadFile = File(...)):
# 	# Create random filename for the uploaded image
# 	letter = string.ascii_letters
# 	random_suffix = ''.join(random.choice(letter) for i in range(5))

# 	new_filename = f'_{random_suffix}.'.join(image.filename.rsplit('.', 1))
# 	path = f'images/{new_filename}'

# 	with open(path, 'w+b') as stream:
# 		shutil.copyfileobj(image.file, stream)

# 	return {
# 		'status': 200,
# 		'filename': path
# 	}
