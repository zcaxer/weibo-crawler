import mysql.connector as mysql

cnx = mysql.connect(user='levi', password='wsx',
                    host='45.63.5.130', database='mysql')
cursor=cnx.cursor()
query=("SELECT user,host FROM user")

cursor.execute(query)

for i,j in cursor:
    print(i,j)

cursor.close()
cnx.close()
