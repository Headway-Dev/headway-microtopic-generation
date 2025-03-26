from fastapi import FastAPI

from src import routers


app = FastAPI()
app.include_router(routers.topics.router)