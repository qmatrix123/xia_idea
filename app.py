import streamlit as st
from time import sleep
import base64

# 编码函数
def encrypt_employee_id(employee_id):
    encrypted_id = base64.b64encode(employee_id.encode()).decode()
    return encrypted_id

# 解码函数
def decrypt_employee_id(encrypted_id):
    decrypted_id = base64.b64decode(encrypted_id.encode()).decode()
    return decrypted_id

def log_in():
    st.session_state["logged_in"] = True
    st.success("Logged in!")
    sleep(0.5)
    st.switch_page("pages/user.py")

def log_out():
    st.session_state["logged_in"] = False
    st.success("Logged out!")
    sleep(0.5)

if "id" in st.query_params:
    encrypted_username = st.query_params["id"]
    st.session_state["id"] = encrypted_username
    st.session_state["logged_in"] = True
    st.switch_page("pages/user.py")

username = st.text_input("员工编号", key="username")

if st.button("登录", key="login_button", help="点击此按钮以登录", use_container_width=True):
    if not st.session_state.get("logged_in", False):
        if username != "" and len(username) == 7:
            # 加密员工编号
            encrypted_username = encrypt_employee_id(username)

            st.session_state["logged_in"] = True
            st.session_state["id"] = encrypted_username
            st.query_params["id"] = encrypted_username
            st.success("Logged in!")
            sleep(0.5)
            st.switch_page("pages/user.py")
    else:
        st.write("Logged in!")
        st.button("log out", on_click=log_out)

if "id" in st.session_state and st.session_state["id"] == "test":
    st.session_state["logged_in"] = True
    st.switch_page("pages/user.py")
