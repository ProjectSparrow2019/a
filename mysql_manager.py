import mysql.connector
from product import Product

class MySQLManager:
    _host="localhost"
    _user="root"
    _password=""
    _database="sparrow"

    def connectMySQL(self,host=None,user=None,passwd=None,database=None):
        return mysql.connector.connect(host=host,user=user,passwd=passwd,database=database)

    def connectDefaultMySQL(self):
        return mysql.connector.connect(host=self._host,user=self._user,passwd=self._password,database=self._database)

    def saveResults(self, connection=None, products=None):
        cursor = connection.cursor()
        for x in products:
            print(x.predict)
            sql = "INSERT INTO produto (title,price,description,author,predict,percentual,link) values('"+x.title+"',"+str(x.price)+",'"+x.description+"','"+x.author+"','"+x.predict+"',"+str(x.percentual)+",'"+x.link+"')"
            cursor.execute(sql)
        connection.commit()

    def findProductBase(self,connection=None, productName=None):
        cursor = connection.cursor()
        sql = "SELECT title,author,description,price,predict FROM base WHERE title LIKE '%" +productName+ "%'"
        cursor.execute(sql)
        return cursor.fetchall()

    def findMinorPrice(self,connection=None,productName=None):
        cursor = connection.cursor()
        sql = "SELECT MIN(price) FROM base WHERE title LIKE '%" +productName+ "%' AND predict = 'verdadeiro'"
        cursor.execute(sql)
        return cursor.fetchone()