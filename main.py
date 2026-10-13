# objective: get all the activities
from fastapi import FastAPI
import database as DB

app = FastAPI(title="PulseTrack")
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
def get_activities():
    return {"users" : DB.get_users()}