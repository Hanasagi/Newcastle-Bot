import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

class DAO:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.database = 'alship'
        self.password = ''
        self.connection = ''
        self.cursor=''
        self.connect()

    def connect(self):
        try:
            connection = mysql.connector.connect(host=self.host,
                                                 user=self.user,
                                                 use_unicode=True,
                                                 charset='utf8',
                                                 database=self.database,
                                                 password=self.password)

            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                self.connection = connection
                self.setCursor()
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            else:
                print(err)

    def setCursor(self):
            self.cursor = self.connection.cursor(buffered=True)

    def insert(self,DBName,Attribut=[],Value=[]):
        attribList = ""
        valueList = ""
        numberOfValue=""
        for i, j in zip(Attribut, Value):
            attribList += i + ','
            numberOfValue += "%s,";
        attribList= attribList[:-1]
        numberOfValue=numberOfValue[:-1]
        sql=("""INSERT INTO {}({}) VALUES({})""").format(DBName,attribList,numberOfValue)
        self.cursor.execute(sql,Value)
        self.connection.commit()

    def select(self,DBName,Attribut=[],AttribWhere="",ValueWhere=""):
        attribList = ""
        for i in Attribut:
            attribList += i + ','
        attribList = attribList[:-1]
        if AttribWhere!="" :
            sql = ("""SELECT {} FROM {} WHERE {}=%s""").format(attribList, DBName, AttribWhere)
            self.cursor.execute(sql, (ValueWhere,))
        else:
            sql = ("""SELECT {} FROM {}""").format(attribList, DBName)
            self.cursor.execute(sql)

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Disconnected")

