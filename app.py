from fastapi import FastAPI

from modules.controller import router as livre_router

app = FastAPI(title="Livre API")

app.include_router(livre_router)