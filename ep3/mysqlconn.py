# pip install mysql-connector-python
import mysql.connector

cnx = mysql.connector.connect(user='pyuser', password='<password>',
                              host='127.0.0.1',
                              database='world')
cursor = cnx.cursor()

query = ("SELECT * FROM COUNTRY")

cursor.execute(query)

row = cursor.fetchone()

while row:
    print(row)
    row = cursor.fetchone()

print()
columns = [column[0] for column in cursor.description]
print(columns)

cursor.close()
cnx.close()