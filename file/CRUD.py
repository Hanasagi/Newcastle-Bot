import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode

class CRUD:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.database = 'newcastle'
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

    def create(self,DBName,Attribut=[],Type=[]):
        attribList=""
        for i, j in zip(Attribut,Type):
            attribList+=i+" "+j+","
        sql=("""CREATE TABLE {}({})""").format(DBName,attribList[:-1])
        self.cursor.execute(sql)
        self.connection.commit()

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

    def update(self, DBName, Attribut=[], Value=[], AttribWhere="",ValueWhere="" ):
        attribList = ""
        valueList = ""
        numberOfValue = ""
        for i, j in zip(Attribut, Value):
            attribList += i + '=' + j +','
            numberOfValue += "%s,";
        attribList = attribList[:-1]
        numberOfValue = numberOfValue[:-1]
        if AttribWhere!="" :
            sql = ("""UPDATE {} SET {} WHERE {}=%s""").format(DBName, attribList, AttribWhere)

            self.cursor.execute(sql, (ValueWhere,))
        else:
            sql = ("""SELECT {} FROM {}""").format(attribList, DBName)
            self.cursor.execute(sql)
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

    def delete(self,DBName,AttribWhere="",ValueWhere=""):
        if AttribWhere != "":
            sql = ("""DELETE FROM {} WHERE {}=%s""").format(DBName, AttribWhere)
            self.cursor.execute(sql, (ValueWhere,))
        else:
            sql = ("""DELETE FROM {}""").format( DBName)
            self.cursor.execute(sql)

    def drop(self,DBName):
        sql = ("""DROP TABLE {}""").format(DBName)
        self.cursor.execute(sql)
        self.connection.commit()

    def get_timestamp(self,dbName,tableName):
        sql = ("""SELECT UPDATE_TIME FROM information_schema.tables WHERE  TABLE_SCHEMA = '{}' AND TABLE_NAME = '{}'""").format(dbName,tableName)
        self.cursor.execute(sql)

    def close(self):
        self.cursor.close()
        self.connection.close()
        print("Disconnected")

