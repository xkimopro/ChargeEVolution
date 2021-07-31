import mysql.connector

def openConnection():
    try:
        mydb = mysql.connector.connect(host="localhost", user="root", password="", database="chargeevolution")
    except Exception as e:
        return {"status": 500, "msg": "Database unavailable"}
    mycursor = mydb.cursor(buffered=True)
    return [mycursor, mydb]

def closeConnection(mydb, mycursor):
    mydb.close()
    mycursor.close()
