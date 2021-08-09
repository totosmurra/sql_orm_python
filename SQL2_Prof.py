import os
import csv
import sqlite3
import json
import requests



def create_schema():
    conn = sqlite3.connect('MELI.db')

    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS DatosMendoza;
            """)

    c.execute("""
            CREATE TABLE DatosMendoza(
                [id] TEXT PRIMARY KEY,
                [site_id] TEXT,
                [title] TEXT,
                [price] INTEGER,
                [currency_id] TEXT,
                [initial_quantity] INTEGER,
                [available_quantity] INTEGER,
                [sold_quantity] INTEGER

            );
            """)

    conn.commit()

    conn.close()
    

def fill():
    
    conn = sqlite3.connect('MELI.db')
    c = conn.cursor()
    
    archivo = "meli_technical_challenge_data.csv"

    csvfile = open(archivo)
    
    data = list(csv.DictReader(csvfile))

    csvfile.close()

    lista_con_ids = []

    for v in data:
        s = v["site"]
        i = v["id"]

        try:
            s = str(s)
            i = str(i)
        except:
            print("No tendría que funcionar mal pero lo hizo pq si :b")
    
        x = s + i

        lista_con_ids.append(x)



    for i in lista_con_ids:
        
        
        URL = "https://api.mercadolibre.com/items?ids="+i
        response = requests.get(URL).json()
        datos = response[0]["body"]


            
        for asd in datos:
                    
                #datos_utiles = {"id":x["id"], "site_id":x["site_id"], "title":x["title"], "price":x["price"], "currency_id":x["currency_id"], "initial_quantity":x["initial_quantity"], "available_quantity":x["available_quantity"], "sold_quantity":x["sold_quantity"]}
                #datos_utiles = x["id"], x["site_id"], x["title"], x["price"], x["currency_id"], x["initial_quantity"], x["available_quantity"], x["sold_quantity"]
            #try:        
                id1 = (datos["id"])
                site_id1 = (datos["site_id"])
                title1 = (datos["title"])
                price1 = (datos["price"])
                currency_id1 = (datos["currency_id"])
                initial_quantity1 = (datos["initial_quantity"])
                available_quantity1 = (datos["available_quantity"])
                sold_quantity1 = (datos["sold_quantity"])

                #dataset = (id, site_id, title, price, currency_id, initial_quantity, available_quantity, sold_quantity)

                #dataset = [{i["id"]}, {i["site_id"]}, {i["title"]}, {i["price"]}, {i["currency_id"]}, {i["initial_quantity"]}, {i["available_quantity"]}, {i["sold_quantity"]}]

                dataset = [id1],[site_id1],[title1],[price1],[currency_id1],[initial_quantity1],[available_quantity1],[sold_quantity1]
                    
                conn = sqlite3.connect('MELI.db')

                c = conn.cursor()

                
                c.executemany   ("""INSERT INTO DatosMendoza id, site_id, title,price, currency_id, initial_quantity, available_quantity, sold_quantity 
                                VALUES (?,?,?,?,?,?,?,?)""", dataset)

                conn.commit()
            
            #except:
                #continue
        


        
        
        
        
    print ("Agarre de datos importantes finalizado")

    c.execute('SELECT * FROM DatosMendoza')
    
    while True:
        row = c.fetchone()
        if row is None:
            break
        print(row)

    conn.close()

    print("Relleno de la tabla finalizado")






if __name__ == "__main__":
    print("Comienzo del programa")

    create_schema()

    fill()

