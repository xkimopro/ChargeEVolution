import mysql.connector

try :
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="chargeevolution"
  )
  mycursor = mydb.cursor(buffered=True)
except Exception as e:
  print("Connection is down")

  

