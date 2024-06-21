import streamlit as st
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
import base64
import pytz

shanghai_tz = pytz.timezone('Asia/Shanghai')

# 解码函数
def decrypt_employee_id(encrypted_id):
    decrypted_id = base64.b64decode(encrypted_id.encode()).decode()
    return decrypted_id


# 数据库连接字符串
DATABASE_URI = 'postgresql://idea_owner:K7et2ERyJBqk@ep-tight-paper-a1dw4ef8.ap-southeast-1.aws.neon.tech/idea?sslmode=require'

# 创建数据库引擎和会话
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# 定义想法数据模型
class Idea(Base):
    __tablename__ = 'ideas'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    title = Column(String)
    description = Column(String)
    employee_id = Column(String)
    status = Column(String)
    remark = Column(String)

# 创建数据库表（如果不存在）
Base.metadata.create_all(engine)

# 定义展示想法页面
def show_ideas_page():
    st.title('小想法，大智慧')

    st.header('提交新想法')
    title = st.text_input('标题')
    description = st.text_area('描述')
    employee_id = decrypt_employee_id(st.session_state.get("id"))

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button('提交想法', key='submit_button', help='提交您的想法', use_container_width=True):
            timestamp = datetime.now(shanghai_tz)
            print(timestamp)
            new_idea = Idea(timestamp=timestamp, title=title, description=description,
                            employee_id=employee_id, status='待处理', remark='')

            session = Session()
            session.add(new_idea)
            session.commit()
            session.close()

            st.success('您的想法已成功提交, 管理员稍后会尽快处理!')

    # 从数据库中加载已提交的想法
    session = Session()
    submitted_ideas = session.query(Idea).filter_by(employee_id=employee_id).order_by(Idea.timestamp.desc()).all()
    session.close()

    if submitted_ideas:
        st.markdown("<h3></h3>", unsafe_allow_html=True)

        for idea in submitted_ideas:
            formatted_timestamp = idea.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # 格式化时间戳

            st.write(f"### {idea.title}")
            st.markdown(f"**描述:** {idea.description}")
            st.write(f"**状态:** {idea.status}")
            st.write(f"**备注:** {idea.remark}")
            st.write(f"**时间:** {formatted_timestamp}")
            st.write("---")

    else:
        st.info('暂无已提交的想法。')

def log_out():
    st.session_state["logged_in"] = False
    del st.session_state.id
    del st.query_params.id

if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
    st.switch_page("app.py")

if "id" in st.session_state:
    st.query_params["id"] = st.session_state["id"]

st.button("log out", on_click=log_out)

show_ideas_page()
