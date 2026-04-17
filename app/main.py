from fastapi import FastAPI
from app.agent import run_agent

app = FastAPI()

@app.get("/search")
def search(q: str):
    return run_agent(q)
