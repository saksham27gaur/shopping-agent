import streamlit as st
import requests

st.title("🛒 Autonomous Shopping Assistant")

query = st.text_input("Search for products")

if st.button("Search"):

    res = requests.get(f"http://shopping-agent-backend-1:8000/search?q={query}")
    data = res.json()

    # ✅ Summary
    st.subheader("🧠 AI Recommendation")
    st.write(data["summary"])

    # ✅ Products
    st.subheader("🏆 Top Products")

    if data["top_products"]:
        for i, p in enumerate(data["top_products"], 1):
            st.markdown(f"""
            ### {i}. {p['title']}
            💰 Price: ₹{p['price']}  
            ⭐ Rating: {p['rating']}
            """)
    else:
        st.warning("No products found")

    # ✅ Agent thinking (VERY IMPRESSIVE FOR DEMO)
    with st.expander("⚙️ How the AI thinks"):
        st.text(data["agent_steps"])