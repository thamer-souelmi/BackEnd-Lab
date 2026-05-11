from fastapi import APIRouter, HTTPException
from auth.jwt import create_token
from pydantic import BaseModel


router = APIRouter()

# fake user for now (later connect DB)
fake_user = {
    "email": "admin@test.com",
    "password": "1234"
}

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(payload: LoginRequest):
    if payload.email != fake_user["email"] or payload.password != fake_user["password"]:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"email": payload.email})
    return {"access_token": token, "token_type": "bearer"}

