import pyodbc

server = '127.0.0.1'
db = 'world'
driver = 'MySQL ODBC 8.1 Unicode Driver'
uid = 'pyuser'
pwd = '<password>'

conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={db};UID={uid};PWD={pwd}')
cursor = conn.cursor()
cursor.execute('Select * from country')

row = cursor.fetchone()

while row:
    print(row)
    row = cursor.fetchone()

print()
columns = [column[0] for column in cursor.description]
print(columns)