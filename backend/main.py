from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from database.db_setup import engine
from database import db_models
from routers import article


app = FastAPI(
	title="Blog Post",
	version="0.1.0"
)

# Database Models
db_models.Base.metadata.create_all(engine)

# Mount endpoints
app.include_router(article.router)

# Mount static directory
# app.mount(
# 	'/images',
# 	StaticFiles(directory='images'),
# 	name='images'
# )

# CORS middleware
origin = ['http://localhost:3000']
app.add_middleware(
	CORSMiddleware,
	allow_origins=origin,
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*']
)