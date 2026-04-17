import requests
from app.tools import search_products, rank_products

OLLAMA_URL = "http://ollama:11434/api/generate"

def call_llm(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": "llama3.2:3b",
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]


def run_agent(user_query):
    history = []

    # Step 1: Plan
    plan_prompt = f"""
    You are an AI shopping assistant.

    User query: {user_query}

    Break this into steps:
    1. Search products
    2. Compare them
    3. Recommend best

    Output steps.
    """

    plan = call_llm(plan_prompt)
    history.append(plan)

    # Step 2: Act → Search
    products = search_products(user_query)

    # Step 3: Observe + Reason
    reasoning_prompt = f"""
    User query: {user_query}

    Products:
    {products}

    Compare and recommend best 3 with reasons.
    """

    result = call_llm(reasoning_prompt)

    # Step 4: Rank (extra logic)
    ranked = rank_products(products)

    return {
        "plan": plan,
        "recommendation": result,
        "ranked": ranked
    }
