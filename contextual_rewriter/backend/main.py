# Placeholder for FastAPI routes
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from rewriter import rewrite_text
from database import SessionLocal, User, RewriteHistory

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Models
class UserRequest(BaseModel):
    username: str
    password: str

class RewriteRequest(BaseModel):
    text: str
    context: str
    username: str

@app.post("/register")
def register(user: UserRequest):
    db = SessionLocal()
    if db.query(User).filter_by(username=user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = User(username=user.username, password=user.password)
    db.add(db_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: UserRequest):
    db = SessionLocal()
    db_user = db.query(User).filter_by(username=user.username, password=user.password).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.post("/rewrite")
def rewrite(req: RewriteRequest):
    db = SessionLocal()
    user = db.query(User).filter_by(username=req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = rewrite_text(req.text, req.context)

    history = RewriteHistory(
        input_text=req.text,
        output_text=result,
        context=req.context,
        user=user
    )
    db.add(history)
    db.commit()

    return {"rewritten": result}

@app.get("/history/{username}")
def get_history(username: str):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return [
        {
            "input": h.input_text,
            "output": h.output_text,
            "context": h.context,
            "created_at": h.created_at
        }
        for h in user.rewrites
    ]
