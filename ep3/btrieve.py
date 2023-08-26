import pyodbc

server = '127.0.0.1'
database = 'DEMODATA'

conn = pyodbc.connect(f'DRIVER=Pervasive ODBC Interface;SERVERNAME={server};DBQ={database}')
cursor = conn.cursor()
cursor.execute('Select * from Class')

row = cursor.fetchone()

while row:
    print(row)
    row = cursor.fetchone()

print()
columns = [column[0] for column in cursor.description]
print(columns)