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


# def run_agent(user_query):
#     history = []

#     # Step 1: Plan
#     plan_prompt = f"""
#     You are an AI shopping assistant.

#     User query: {user_query}

#     Break this into steps:
#     1. Search products
#     2. Compare them
#     3. Recommend best

#     Output steps.
#     """

#     plan = call_llm(plan_prompt)
#     history.append(plan)

#     # Step 2: Act → Search
#     products = search_products(user_query)

#     # Step 3: Observe + Reason
#     reasoning_prompt = f"""
#     User query: {user_query}

#     Products:
#     {products}

#     Compare and recommend best 3 with reasons.
#     """

#     result = call_llm(reasoning_prompt)

#     # Step 4: Rank (extra logic)
#     ranked = rank_products(products)

#     return {
#         "plan": plan,
#         "recommendation": result,
#         "ranked": ranked
#     }

def run_agent(user_query):
    history = ""
    observation = ""

    for step in range(5):  # limit steps

        prompt = f"""
You are an autonomous shopping agent.

You must follow this format strictly:

Thought: what you think
Action: search_products OR rank_products OR finish
Action Input: input for the action

Action: finish
Action Input: must contain a final recommendation (DO NOT return None)

User Query: {user_query}

Previous steps:
{history}

Observation:
{observation}

Respond in EXACT format:
"""
        print("\nLLM PROMPT:\n", prompt)
        response = call_llm(prompt)

        print("\nLLM RESPONSE:\n", response)

        # Parse response
        try:
            thought = extract(response, "Thought:")
            action = extract(response, "Action:")
            action_input = extract(response, "Action Input:")
        except:
            return {"error": "Parsing failed", "raw": response}

        history += f"\n{response}\n"

# Execute action
        if action == "search_products":
            last_products = search_products(user_query)
            observation = str(last_products)

        elif action == "rank_products":
            products = last_products
            ranked = rank_products(products)
            last_products = ranked
            observation = str(ranked)

        elif action == "finish":
            return {
                "summary": action_input,
                "steps": history,
                "products": last_products if 'last_products' in locals() else []
            }

        else:
            observation = "Unknown action"

    return {"error": "Max steps reached", "steps": history}


def extract(text, key):
    for line in text.split("\n"):
        if line.strip().startswith(key):
            return line.replace(key, "").strip()
    return ""