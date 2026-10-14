# objective: get all the activities
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import database as DB

app = FastAPI(title="PulseTrack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # exact: scheme + host + port
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome"}

@app.get("/hello/{name}")
def say_hello(name: str):
    text = f"Hello {name}"
    return {"greeting": text}

@app.get("/activities")
def get_activities():
    return {"activities" : DB.get_activities()}

@app.get("/users")
def get_users():
    return {"users" : DB.get_users()}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    deleted = DB.delete_user(user_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted": user_id}