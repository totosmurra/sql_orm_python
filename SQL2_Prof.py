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
                [id] INTEGER PRIMARY KEY,
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

    
    lista_con_datos = []


    for i in lista_con_ids:
        URL = "https://api.mercadolibre.com/items?ids="+i
        response = requests.get(URL)
        datos = response.json()

        try:
            for x in datos:
                #datos_utiles = {"id":x["id"], "site_id":x["site_id"], "title":x["title"], "price":x["price"], "currency_id":x["currency_id"], "initial_quantity":x["initial_quantity"], "available_quantity":x["available_quantity"], "sold_quantity":x["sold_quantity"]}
                datos_utiles = {x["id"], x["site_id"], x["title"], x["price"], x["currency_id"], x["initial_quantity"], x["available_quantity"], x["sold_quantity"]}
                lista_con_datos.append(datos_utiles)

        except:
            continue
        
    print ("Agarre de datos importantes finalizado")

    conn = sqlite3.connect('MELI.db')

    c = conn.cursor()

    
    for i in lista_con_datos:

        dataset = [{i["id"]}, {i["site_id"]}, {i["title"]}, {i["price"]}, {i["currency_id"]}, {i["initial_quantity"]}, {i["available_quantity"]}, {i["sold_quantity"]}]

        c.executemany   ("""INSERT INTO DatosMendoza (id, site_id, title, price, currency_id, initial_quantity, available_quantity, sold_quantity)
                        VALUES (?,?,?,?,?,?,?,?);""", dataset)
    
    
    conn.commit()

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

