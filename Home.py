import streamlit as st
import datetime
import pandas as pd
import pymysql

class mysqlDB():

    def connectDB(self, host, user, password, database):
        self.myhost = host
        self.myuser = user
        self.mypassword = password
        self.mydatabase = database
        self.connection = pymysql.connect(host=self.myhost,
                                          user=self.myuser,
                                          password=self.mypassword,
                                          database=self.mydatabase,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

        return self.connection

    def readBySQL(self, sql):
        with self.connection.cursor() as cursor:
            # Read table list
            cursor.execute(sql)
            result = cursor.fetchall()
            
        return result


st.set_page_config(
    page_title="Elevator IoT",
    page_icon="👋",
)


st.write("# 엘리베이터 IoT - New 👋")

st.markdown(
    """
    엘리베이터 IoT 시스템의 일련의 프로그램을 사용할 수 있습니다.
    **👈 사이드바에 있는 기능을 선택하세요.** 필요한 기능들을 이용할 수 있습니다.
"""
)


st.header("메뉴판")
topicA = st.selectbox("Elevator number",
                              ("Elevator001", "Elevator002", "Elevator003", "Elevator004", "Elevator005", "Elevator006", "Elevator007", "Elevator008"))
topicB = st.selectbox("Sensor",("decibel", "Xmax", "Ymax", "Zmax"))
TopicT = topicA + "/" + topicB

if 'selected_date' not in st.session_state:
    st.session_state['selected_date'] = datetime.date(2022,9,1)
seldate = st.session_state['selected_date']
seldate = st.date_input("Date", seldate)

isImporting = st.button("주문하기")


if isImporting:
    sql = "select timestamp, data from elevatortb "
    sql += "where topic = '{}' and DATE(timestamp) = DATE('{}') ".format(TopicT, seldate)
    sql += "order by timestamp asc;"
    st.write(sql)

    thisDB = mysqlDB()
    thisDB.connectDB(
        host='dkswiot.iptime.org',
        user='dksw',
        password='dksw31512',
        database='dkswiotDB')
    thisResult = pd.DataFrame(thisDB.readBySQL(sql))
    st.write(thisResult)
    st.line_chart(thisResult.rename(columns={'timestamp':'index', 'data':TopicT}).set_index('index'))
