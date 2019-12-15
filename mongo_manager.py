import pymongo
from product import Product

class MongoManager:
    _mongo_address="mongodb://localhost:27017"
    _database='sparrow'
    _collection='gotProducts'

    def connectMongo(self,mongo_address=None,database=None):
        return pymongo.MongoClient(mongo_address)[database]

    def getProducts(self,mongoConnection=None, collection=None):
        return mongoConnection[collection].find()

    def clearMongo(self,mongoConnection=None, collection=None):
        mongoConnection[collection].delete_many({})

    def insertProducts(self,products=None,mongoConnection=None, collection=None):
        return mongoConnection[collection].insert_one(products)


#insert example
#mongo_ = MongoManager()
#connection = mongo_.connectMongo(mongo_._mongo_address,mongo_._database)
p =    [
    {"link":"https://sp.olx.com.br/sao-paulo-e-regiao/bijouteria-relogios-e-acessorios/relogio-invicta-yakuza-s1-original-687332267?xtmc=rel%C3%B3gio+invicta+yakuza&xtnp=1&xtcr=15", 
    "codigo_screenshot":"MMjlSp", 
    "author":"Fioravante-junior", 
    "data":"Publicado em 20/11 as 00:31", 
    "title":"Relogio invicta Yakuza S1 original", 
    "description":"Invicta Yakuza S1 original, importado da Italia, quase 01 ano de uso. Tem todos os certificados e caix",
     "price":980, 
     "condicao":"Usado", 
     "tag_suspeita":"r\u00e9plica", 
     "categoria":"Categoria\nBijouterias, relogios e acessorios", 
     "localizacao":"Sao Paulo\nSao Paulo e regiao\nBijouterias, relogios e acessorios\nOutras cidades\nSuzano"}
 ]
#mongo_.insertProducts(products=p,mongoConnection=connection,collection=mongo_._collection)
#mongo_.clearMongo(mongoConnection=connection,collection=mongo_._collection)
#x = mongo_.getProducts(mongoConnection=connection,collection=mongo_._collection)
#print(x)

#for y in x:
 #   print(y['title'])