from product import Product

class DatabaseUtil:

    def marshallingDataToObject(self,data_products=None, onlyPredict=False, isMongoDB=False):
        object_products = []
        for x in data_products:
            product = Product()

            if(isMongoDB == False):
                if(onlyPredict == False):
                    product.title = x[0]
                    product.author = x[1]
                    product.description = x[2]
                    product.price = x[3]
                    product.link = x[4]
                else:
                    product.predict = x[4]

            else:
                product.title = x['title']
                product.author = x['author']
                product.description = x['description']
                product.price = x['price']
                product.link = x['link']
            object_products.append(product)
        return object_products

    def closeConnection(self,connection=None):
        connection.close()