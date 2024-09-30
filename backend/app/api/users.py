from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/signup")
async def signup():
    return {"message": "signed up"}


@router.post("/login")
async def login():
    return {"message": "logged in"}
