from st_pages import hide_pages
from time import sleep
import streamlit as st


def log_in():
    st.session_state["logged_in"] = True
    hide_pages([])
    st.success("Logged in!")
    sleep(0.5)
    st.switch_page("pages/user.py")


def log_out():
    st.session_state["logged_in"] = False
    st.success("Logged out!")
    sleep(0.5)


if "id" in st.query_params:
    st.session_state["id"] = st.query_params["id"]
    st.session_state["logged_in"] = True
    st.switch_page("pages/user.py")

if not st.session_state.get("logged_in", False):
    hide_pages(["page1", "page2", "page3"])
    username = st.text_input("Username", key="username")
    password = st.text_input("Password", key="password", type="password")

    if username == "test" and password == "test":
        st.session_state["logged_in"] = True
        st.session_state["id"] = "test"
        st.query_params["id"] = "test"
        hide_pages([])
        st.success("Logged in!")
        sleep(0.5)
        st.switch_page("pages/user.py")

else:
    st.write("Logged in!")
    st.button("log out", on_click=log_out)

if "id" in st.session_state and st.session_state["id"] == "test":
    st.session_state["logged_in"] = True
    st.switch_page("pages/user.py")