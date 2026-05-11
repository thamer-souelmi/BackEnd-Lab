from fastapi import FastAPI

from modules.controller import router as livre_router
from auth.router import router as auth_router


app = FastAPI(title="Livre API")

app.include_router(livre_router)
app.include_router(auth_router)