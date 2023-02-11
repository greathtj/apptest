import streamlit as st
import datetime
import pandas as pd
import customLib as cl

def dailyInfo():
    topicA = st.selectbox("Elevator number - day",
                        ("Elevator001", "Elevator002", "Elevator003", "Elevator004", "Elevator005", "Elevator006", "Elevator007", "Elevator008"))
    topicB = st.selectbox("Sensor - day",("decibel", "Xmax", "Ymax", "Zmax"))
    TopicT = topicA + "/" + topicB

    if 'selected_date' not in st.session_state:
        st.session_state['selected_date'] = datetime.date(2022,9,1)
    seldate = st.session_state['selected_date']
    seldate = st.date_input("Date", seldate)

    isImporting = st.button("주문하기")

    if isImporting:
        st.write(
            """신선한 데이터를 제공하고자 주문과 함께 작업에 들어가므로, 나오기까지 다소 시간이 걸릴 수 있습니다."""
        )
        st.write(
            """이해해주셔서 감사합니다. <종업원>"""
        )

        sql = "select timestamp, data from elevatortb "
        sql += "where topic = '{}' and DATE(timestamp) = DATE('{}') ".format(TopicT, seldate)
        sql += "order by timestamp asc;"
        st.write(sql)

        thisDB = cl.mysqlDB()
        thisDB.connectDB(
            host=st.secrets["DB_Address"],
            database=st.secrets["DB_Name"],
            user=st.secrets["DB_UserName"],
            password=st.secrets["DB_PassWord"]
        )
        thisResult = pd.DataFrame(thisDB.readBySQL(sql))

        if len(thisResult) > 0:
            st.write(thisResult)
            st.line_chart(thisResult.rename(columns={'timestamp':'index', 'data':TopicT}).set_index('index'))

            st.write(
                """
                Here they are... Enjoy your data... We are very happy to be of your service...
                """
            )
        else:
            st.write("Sorry, but No data...")

def AnalysisPeriod():
    topicA = st.selectbox("Elevator number - analysis",
                        ("Elevator001", "Elevator002", "Elevator003", "Elevator004", "Elevator005", "Elevator006", "Elevator007", "Elevator008"))
    topicB = st.selectbox("Sensor - analysis",("decibel", "Xmax", "Ymax", "Zmax"))
    TopicT = topicA + "/" + topicB

    if 'start_date' not in st.session_state:
        st.session_state['start_date'] = datetime.date(2022,9,1)
    startDate = st.session_state['start_date']
    StartDate = st.date_input("Start Date", startDate)

    if 'end_date' not in st.session_state:
        st.session_state['end_date'] = datetime.datetime.now().date()
    endDate = st.session_state['end_date']
    endDate = st.date_input("End Date", endDate)


st.set_page_config(
    page_title="Elevator IoT",
    page_icon="👋",
)


st.write("# 엘리베이터 IoT - 맛집 👋")

st.markdown(
    """
    엘리베이터 IoT 시스템의 일련의 프로그램을 사용할 수 있습니다.
    **아래 메뉴판에 있는 기능을 취항껏 주문해주세요.** 필요한 기능들을 이용할 수 있습니다.
"""
)

st.header("메뉴판")

tab1, tab2, tab3 = st.tabs(["전체요리 - 일별데이터", "메인요리 - 평균, 분산 등", "후식 - 아노말리"])

with tab1:
   st.header("전체요리 - 일별데이터")
   dailyInfo()

with tab2:
   st.header("메인요리 - 평균, 분산 등")
   AnalysisPeriod()

with tab3:
   st.header("후식 - 아노말리")


