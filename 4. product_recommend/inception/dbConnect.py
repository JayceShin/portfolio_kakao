import sqlite3


class Con:

    def insert(self, result):

        con = sqlite3.connect("/Users/shinkangsik/django/GalleriaAPI/galAPI/db.sqlite3")
        cur = con.cursor()

        sql1 = "insert into inception_recommendresult(image, item, result, time) values (?, ?, ?, ?);"
        con.execute(sql1, result)

        con.commit()
        con.close()


    def insertResult(self, param):
        con = sqlite3.connect("/Users/shinkangsik/django/GalleriaAPI/galAPI/db.sqlite3")
        cur = con.cursor()

        sql2 = "insert into inception_joinlist (item, price, stock, store, phone, result, itemName, storeName, time) select A.item, A.price, A.stock, A.store, A.phone, B.result, A.itemName, A.StoreName, B.time from inception_itemlist A, inception_recommendresult B where replace(A.item, '_', ' ')= B.item and B.image = ? and B.time = ?;"

        con.execute(sql2, param)

        con.commit()
        con.close()


    def selectProduct(self):
        con = sqlite3.connect("/Users/shinkangsik/django/GalleriaAPI/galAPI/db.sqlite3")
        cur = con.cursor()
        kang = ()
        for row in con.execute("select item from inception_itemlist"):
            kang += row

        con.close()
        return kang