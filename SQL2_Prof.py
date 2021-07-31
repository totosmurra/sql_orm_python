import os
import csv
import sqlite3




def create_schema():
    conn = sqlite3.connect('MELI.db')

    c = conn.cursor()

    c.execute("""
                DROP TABLE IF EXISTS DatosMendoza;
            """)

    c.execute("""
            CREATE TABLE DatosMendoza(
                [id] INTEGER PRIMARY KEY,
                [name] TEXT NOT NULL,
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


    



if __name__ == "__main__":
    print("Comienzo del programa")
