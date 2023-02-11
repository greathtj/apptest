import pymysql

class mysqlDB():

    def connectDB(self, host, database, user, password):
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
