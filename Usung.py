import streamlit as st
import pymysql
import datetime
import pandas as pd
import streamlit.components.v1 as components
import altair as alt

# modules sub routines ==================================================================

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

def showDailyInfo():
    if st.button("최근 1주일"):
        viewEnd = datetime.datetime.now().date()
        viewStart = viewEnd - datetime.timedelta(days=7)
        st.session_state['view_start'] = viewStart
        st.session_state['view_end'] = viewEnd
    if st.button("최근 30일"):
        viewEnd = datetime.datetime.now().date()
        viewStart = viewEnd - datetime.timedelta(days=30)
        st.session_state['view_start'] = viewStart
        st.session_state['view_end'] = viewEnd
    if st.button("최근 180일"):
        viewEnd = datetime.datetime.now().date()
        viewStart = viewEnd - datetime.timedelta(days=180)
        st.session_state['view_start'] = viewStart
        st.session_state['view_end'] = viewEnd        

    if 'view_start' not in st.session_state:
        st.session_state['view_start'] = datetime.datetime.now().date()
    viewStart = st.session_state['view_start']
    thisVS = st.date_input("조회 시작일", viewStart)
    if thisVS:
        viewStart = thisVS
    if 'view_end' not in st.session_state:
        st.session_state['view_end'] = datetime.datetime.now().date()
    viewEnd = st.session_state['view_end']
    thisVE = st.date_input("조회 종료일", viewEnd)
    if thisVE:
        viewEnd = thisVE


    sql = "SELECT STR_TO_DATE(substr(timestamp, 1, 10), '%Y-%m-%d') AS 가동일, "
    # sql += "dayofweek(substr(timestamp, 1, 10), '%Y-%m-%d') as D_week, "
    sql += "dayofweek('2023-02-01') as 요일, "
    sql += "cast(SUM(cast(data/1000 as signed integer))/60 as signed integer) AS 가동시간_분 "
    sql += "FROM dkswiotDB.ysl_machine001_opMillis "
    sql += "where STR_TO_DATE(substr(timestamp, 1, 10), '%Y-%m-%d') between date('{}') and date('{}') ".format(viewStart, viewEnd)
    sql += "GROUP BY 가동일 order by 가동일 desc;"

    # st.write(sql)
    thisResult = thisDB.readBySQL(sql)
    if len(thisResult) > 0:
        thisAllPd = pd.DataFrame(thisResult)
        thisAllPd.set_index('가동일')
        tmp = pd.to_datetime(thisAllPd['가동일'])
        thisAllPd['요일'] = tmp.dt.day_name()

        st.write(thisAllPd)
        # st.bar_chart(thisAllPd.rename(columns={'가동일':'index', '가동시간_분':'가동시간 (분)'}).set_index('index'))
        # st.bar_chart(thisAllPd["가동시간_분"].values)
        chart = alt.Chart(thisAllPd).mark_bar().encode(
            x='가동일',
            y='가동시간_분'
        ).properties(
            width=alt.Step(40) # Set the bar width
        )
        st.altair_chart(chart, use_container_width=True)

def showSelectedDayInfo():
    if 'selected_date' not in st.session_state:
        st.session_state['selected_date'] = datetime.datetime.now().date()
    seldate = st.session_state['selected_date']
    seldate = st.date_input("가동일", seldate)

    sql = "SELECT "
    sql += "cast(SUM(cast(data/1000 as signed integer))/60 as signed integer) AS 가동시간_분 "
    sql += "FROM dkswiotDB.ysl_machine001_opMillis "
    sql += "where STR_TO_DATE(substr(timestamp, 1, 10), '%Y-%m-%d') = '{}';".format(seldate)

    # st.write(sql)
    thisResult = thisDB.readBySQL(sql)
    if len(thisResult) > 0:
        thisPd = pd.DataFrame(thisResult)
        st.write("총 가동시간: ", thisPd['가동시간_분'].values[0], "분")

    sql = "select substr(timestamp, 12, 5) as 시각, "
    sql += "cast(data/1000 as signed integer) as 가동시간_초 "
    sql += "from dkswiotDB.ysl_machine001_opMillis "
    sql += "where date(substr(timestamp, 1, 19)) = '{}' ".format(seldate)
    sql += "order by timestamp asc;"

    # st.write(sql)
    thisResult = thisDB.readBySQL(sql)
    if len(thisResult) > 0:
        thisPd = pd.DataFrame(thisResult)
        thisPd.set_index('시각')

        st.write(thisPd)
        st.line_chart(thisPd.rename(columns={'시각':'index', '가동시간_초':'가동시간 (초)'}).set_index('index'))


# program start =================================================================

thisDB = mysqlDB()
thisDB.connectDB(st.secrets["DB_Address"],
                 st.secrets["DB_User"],
                 st.secrets["DB_PassWord"],
                 st.secrets["DB_Name"]) 

st.set_page_config(
    page_title="유성레이저 IoT",
    page_icon="☄️",
)

st.title("유성레이저 ☄️")
st.subheader("레이저설비 현황")
showDailyInfo()

st.subheader("해당일 가동상황")
showSelectedDayInfo()