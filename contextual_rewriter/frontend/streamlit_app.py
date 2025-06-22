# Placeholder for Streamlit frontend
import streamlit as st
import requests

API_BASE = "http://localhost:8000"

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.history = []

# Registration page
def register():
    st.subheader("🆕 Create an Account")
    with st.form("register"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Register")

        if submit:
            res = requests.post(f"{API_BASE}/register", json={
                "username": username,
                "password": password
            })
            if res.status_code == 200:
                st.success("✅ Registered successfully. You can now log in.")
            else:
                st.error(res.json().get("detail", "Registration failed"))

# Login page
def login():
    st.subheader("🔐 Login")
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

        if submit:
            res = requests.post(f"{API_BASE}/login", json={
                "username": username,
                "password": password
            })
            if res.status_code == 200:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("✅ Logged in successfully")
                st.experimental_rerun()
            else:
                st.error(res.json().get("detail", "Login failed"))

# Rewriter interface
def main_app():
    st.title("📝 Contextual Document Rewriter")
    st.markdown(f"Welcome, **{st.session_state.username}**")

    text = st.text_area("Enter your text:")
    context = st.selectbox("Choose style:", ["Formal", "Casual", "Simplified", "Academic", "Professional"])

    if st.button("🔁 Rewrite Text"):
        if not text.strip():
            st.warning("Please enter some text.")
        else:
            with st.spinner("Rewriting..."):
                res = requests.post(f"{API_BASE}/rewrite", json={
                    "text": text,
                    "context": context,
                    "username": st.session_state.username
                })
                if res.status_code == 200:
                    rewritten = res.json()["rewritten"]
                    st.subheader("🆕 Rewritten Text")
                    st.text_area("Output", rewritten, height=300)

                    # Reload history after writing
                    fetch_history()
                else:
                    st.error("Failed to rewrite text.")

    # Show history
    if st.session_state.history:
        st.markdown("## 📜 Your Rewrite History")
        for i, h in enumerate(reversed(st.session_state.history)):
            st.markdown(f"**{i+1}. Style: {h['context']} | {h['created_at']}**")
            with st.expander("🔍 View"):
                st.markdown(f"**Original:** {h['input']}")
                st.markdown(f"**Rewritten:** {h['output']}")
            st.markdown("---")

    # Logout
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.history = []
        st.experimental_rerun()

# Fetch history from backend
def fetch_history():
    res = requests.get(f"{API_BASE}/history/{st.session_state.username}")
    if res.status_code == 200:
        st.session_state.history = res.json()
    else:
        st.session_state.history = []

# Main logic controller
if not st.session_state.logged_in:
    st.title("🧠 Contextual Document Rewriter")
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Register"])
    with tab1:
        login()
    with tab2:
        register()
else:
    fetch_history()
    main_app()
