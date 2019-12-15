from sklearn.svm import LinearSVC
from mysql_manager import MySQLManager
from util import DatabaseUtil

class IA:
    #Como tomar decisoes!
    #Nome do produto =>     tem palavra do dicionario? Sim = 1, nao = 0
    #Nome do author =>      e oficial? Sim = 1, nao = 0
    #Preco =>               mais caro do que o original? (supondo que o original seja 1000) Sim = 1, nao = 0
    #Descricao =>           tem palavra do dicionario? Sim = 1, nao = 0
    
    key_words = ['aa','aaa','réplica','replica','primeira','linha']
    sklearn = LinearSVC()
    mysql = MySQLManager()
    util_db = DatabaseUtil()
    objectProducts = []

    def trainning(self, productName):
        connection = self.mysql.connectDefaultMySQL() #conecta com o banco
        baseProducts = self.mysql.findProductBase(connection=connection,productName=productName) #obtem a base de dados
        objectsBase = self.util_db.marshallingDataToObject(data_products=baseProducts) #converte em objeto
        self.util_db.closeConnection(connection=connection) #fecha a conexao
        classification = self.classification(objectsBase) #classifica os objetos
        objectsBaseClassification = self.util_db.marshallingDataToObject(data_products=baseProducts,onlyPredict=True) #converte em objeto so a classificacao
        resolvedPredict = self.resolverPredict(objectsBaseClassification,invert=True) #resolve os 'verdadeiro/falso' para '0/1'
        print(classification)
        self.sklearn.fit(classification,resolvedPredict) #treina

    def resolverPredict(self, objects,invert=False):
        resolvedPredict = []
        if(invert != True):
            for obj in objects:
                print(obj)
                if(obj == 1):
                    resolvedPredict.append('falso')
                else:
                    resolvedPredict.append('verdadeiro')
        else:
            for obj in objects:
                if('falso' in obj.predict):
                    resolvedPredict.append(1)
                else:
                    resolvedPredict.append(0)
        return resolvedPredict

    def predict(self, products):
        self.objectProducts = self.util_db.marshallingDataToObject(data_products=products,isMongoDB=True) #converter produto pesquisado em objeto
        arrayProducts = self.classification(self.objectProducts) #classifica os objetos
        print(arrayProducts)
        arrayPredicts = []
        arrayPercentual = []

        for product in arrayProducts:
            predict = self.sklearn.predict([product]) #predicao
            arrayPredicts.append(self.resolverPredict(predict))
            arrayPercentual.append(self.getPercentual(product))

        i = 0
        for obj in self.objectProducts:
            obj.predict = arrayPredicts[i][0]
            obj.percentual = arrayPercentual[i]
            i = i + 1

    def getPercentual(self, array):
        sum = 0
        for i in array:
            sum = sum + i
        return (100 / sum)

    def countWords(self,text):
        splitted = text.split(" ")
        for i in splitted:
            if(i.lower() in self.key_words):
                return 1
        return 0

    def classification(self, products):
        connection = self.mysql.connectDefaultMySQL()
        print(len(products))
        #minorPrice = self.mysql.findMinorPrice(connection=connection,productName=products[0].title)
        minorPrice = 500
        #print(minorPrice)
        author = 'author'

        classification = []
        for product in products:
            data = []
            #titulo
            data.append(self.countWords(product.title))
            #preco
            if(product.price < minorPrice):
                data.append(1)
            else:
                data.append(0)
            #descricao
            data.append(self.countWords(product.description))
            #autor
            if(product.author is author):
                data.append(0)
            else:
                data.append(1)
            classification.append(data)

        self.util_db.closeConnection(connection=connection)
        return classification