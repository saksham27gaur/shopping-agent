from fastapi import FastAPI
from app.agent import run_agent

app = FastAPI()

@app.get("/search")
def search(q: str):
    data = run_agent(q)

    return {
        "query": q,
        "summary": data.get("summary", "No response"),
        "top_products": data.get("products", []),
        "agent_steps": data.get("steps", "")
    }


def format_summary(text):
    return text.replace("**", "").strip()