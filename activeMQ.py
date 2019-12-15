import time
import sys
import machine
from mongo_manager import MongoManager
from mysql_manager import MySQLManager
from util import DatabaseUtil

import stomp

db_util = DatabaseUtil()

class MyListener(stomp.ConnectionListener):
    def on_error(self, headers, message):
        print('received an error "%s"' % message)
    def on_message(self, headers, message):
        print('Iniciou o processamento!')
        ia = machine.IA()
        ia.trainning(message)
        print('Treinamento concluído!')
        mongo = MongoManager()
        connection_mongo = mongo.connectMongo(mongo_address=mongo._mongo_address,database=mongo._database)
        products = mongo.getProducts(mongoConnection=connection_mongo,collection=mongo._collection)
        print('Dados coletados do mongo')
        ia.predict(products)
        mongo.clearMongo(mongoConnection=connection_mongo,collection=mongo._collection)
        print('predições feitas')
        mysql = MySQLManager()
        connection_mysql = mysql.connectDefaultMySQL()
        print(ia.objectProducts[0].link)
        mysql.saveResults(connection=connection_mysql,products=ia.objectProducts)
        print('Finalizou o processamento!')

class ActiveMQ:
    def __init__(self,fila):
        self.fila = fila

    def listener(self):
        print('Ouvindo a fila %s' % (self.fila))
        while(True):
            conn = self.connection()
            conn.subscribe(destination=self.fila, id=1, ack='auto')
            time.sleep(1)
            conn.disconnect()

    def connection(self):
        conn = stomp.Connection()
        conn.set_listener('', MyListener())
        conn.start()
        conn.connect('admin', 'admin', wait=True)
        return conn

    def postSklearn(self,message):
        conn = self.connection()
        conn.send(body=message, destination='sklearn')
        conn.disconnect()




        #comandos mysql
        #manager = MySQLManager()
        #connection = manager.connectMySQL(host=manager._mysql_address,user=manager._user,passwd=manager._password,database=manager._database)
    #    product = Product()
     #   product.author='Invicta'
      #  product.description='réplica originau'
      #  product.title='Zeus'
      #  product.price=26.7
        #manager.saveResults(connection=connection,products=[product])
        #comandos mongo
      #  mongo = MongoManager()
     #   connection = mongo.connectMongo(mongo._mongo_address,mongo._database)
      #  prod = {
       #     "title" : "Teste",
      #      "price" : 0.0,
       #     "author":"eu",
      #      "description": "adaddd"
     #   }
   #     mongo.insertProducts([prod],connection,mongo._collection)
        #mongo.clearMongo(mongoConnection=connection,collection=mongo._collection)
    #    x = mongo.getProducts(mongoConnection=connection,collection=mongo._collection)
     #   y = mongo.marshallingDataToObject(x)
      #  for p in y:
         #   print(p.title)