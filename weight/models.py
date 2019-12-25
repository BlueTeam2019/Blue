import mysql.connector

mysqlPort='3306'

# /HEALTH method
def checkalive():
    alive = True
    config = {
        'user': 'root',
        'password': 'pass',
        'host': '0.0.0.0',
        'port': mysqlPort,
        'database': 'weight',
        'raise_on_warnings': True
        }
    cnx = mysql.connector.connect(**config)
    # if mysql.connector.errors.DatabaseError:      # ASSERT
        # return mysql.connector.errors.DatabaseError
    cursor = cnx.cursor()

    if cursor.execute(""" select * from containers_registered """):
        alive = False   # Return FALSE to the calling method if SQL not reached
    else:
        print("alive is: ", alive)
        for (id, weight, unit) in cursor:
            print(id, weight, unit)
    cursor.close()

    cnx.close()
    return alive

# /BATCH-WEIGHT method
"""
    POST /batch-weight
- file=<filename>
Will upload list of tara weights from a file in "/in" folder. Usually used to accept a batch of new containers. 
File formats accepted: csv (id,kg), csv (id,lbs), json ([{"id":..,"weight":..,"unit":..},...])
"""
def batch_up(batchFile, methods=['POST']):
    # 1- receive file (to be parsed) or filename (to be looked in /in)
    # 2- check if csv or json, to parse correctly
    # 3- maintain a connection to MySQL DB
    # 4- send query (INSERT)