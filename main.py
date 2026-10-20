# objective: get all the activities
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel
import sqlite3

import database as DB

app = FastAPI(title="PulseTrack")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # exact: scheme + host + port
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------
# REQUEST MODELS
# -----------
class ActivityCreate(BaseModel):
    user_id: int
    sport: str
    title: str
    started_at: str
    duration_s: int
    distance_m: float = 0

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

@app.get("/activities/{activity_id}")
def get_activity(activity_id: int):
    activity = DB.get_activity(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@app.post("/activities", status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivityCreate, response: Response):
    try:
        new_id = DB.create_activity(**activity.model_dump())
    except sqlite3.IntegrityError as e:
        # unknown user_id or a violated CHECK constraint (sport, duration_s, distance_m)
        raise HTTPException(status_code=400, detail=str(e))
    response.headers["Location"] = f"/activities/{new_id}"
    return DB.get_activity(new_id)

@app.get("/users")
def get_users():
    return {"users" : DB.get_users()}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    deleted = DB.delete_user(user_id)
    if deleted == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"deleted": user_id}