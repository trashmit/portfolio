import psycopg2
from psycopg2.extras import execute_values

import json
import time

conn = psycopg2.connect("postgresql://doadmin:eRJ3lYhVvBl9GPrT@db-postgresql-lon1-20415-do-user-8118775-0.b.db.ondigitalocean.com:25060/defaultdb?sslmode=require")

cursor = conn.cursor()

#        SELECT * FROM public.images
#cursor.execute('''
#'''
#)



cursor.execute('''
		CREATE table normalauth(
			id varchar(64) primary key,
			pass varchar(64)
			)
               ''')

#b = time.time()
#cursor.execute("SELECT * FROM images WHERE ticker = 'btc'")
#a = cursor.fetchall()
#print(time.time()-b)

#data = ("fart3", 'awesome_url4')
#cursor.execute('''INSERT INTO images (name, url) VALUES (%s, %s)  ''', (data))

#execute_values(cursor,"INSERT INTO images (name, url) VALUES %s",data)
#cursor.execute("DELETE FROM images;")

conn.commit()