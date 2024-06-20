import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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
    employee_name = Column(String)
    employee_id = Column(String)
    department = Column(String)

# 创建数据库表（如果不存在）
Base.metadata.create_all(engine)

# 创建一个空的DataFrame来存储想法
ideas_df = pd.DataFrame(columns=['Timestamp', 'Title', 'Description', 'Employee Name', 'Employee ID', 'Department'])

# 定义展示想法页面
def show_ideas_page():
    st.title('员工想法提交系统')

    st.header('提交新想法')
    title = st.text_input('想法标题')
    description = st.text_area('想法描述')
    employee_name = st.text_input('员工姓名')
    employee_id = st.session_state["id"]
    department = st.selectbox('相关部门', ['技术部门', '市场部门', '生产部门', '财务部门'])

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if st.button('提交想法', key='submit_button', help='提交您的想法', use_container_width=True):
            timestamp = datetime.now()
            new_row = {'Timestamp': timestamp, 'Title': title, 'Description': description,
                        'Employee Name': employee_name, 'Employee ID': employee_id,
                        'Department': department}
            ideas_df.loc[len(ideas_df)] = new_row

            session = Session()
            new_idea = Idea(timestamp=timestamp, title=title, description=description,
                            employee_name=employee_name, employee_id=employee_id, department=department)
            session.add(new_idea)
            session.commit()
            session.close()

            st.success('您的想法已成功提交, 管理员稍后会尽快处理!')
    # 从数据库中加载已提交的想法
    session = Session()
    submitted_ideas = session.query(Idea).filter_by(employee_id=employee_id).all()
    session.close()

    if submitted_ideas:
        submitted_ideas_df = pd.DataFrame([{
            'Timestamp': idea.timestamp,
            'Title': idea.title,
            'Description': idea.description,
            'Employee Name': idea.employee_name,
            'Employee ID': idea.employee_id,
            'Department': idea.department
        } for idea in submitted_ideas])
        st.dataframe(submitted_ideas_df)
    else:
        st.info('暂无已提交的想法。')

def log_out():
    st.session_state["logged_in"] = False
    del st.session_state.id
    del st.query_params.id
    

if "logged_in" not in st.session_state or  st.session_state["logged_in"] == False:
    st.switch_page("app.py")


if "id" in st.session_state:
    st.query_params["id"] = st.session_state["id"]

st.button("log out", on_click=log_out)

show_ideas_page()