import mysql.connector

def checkalive():
    alive = True
    config = {
        'user': 'root',
        'password': 'pass',
        'host': '0.0.0.0',
        'port': '8877',
        'database': 'weight',
        'raise_on_warnings': True
        }
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    print("HELLO from MODELS!")
    # add_employee = ("INSERT INTO weight "
                #    "(first_name, last_name, hire_date, gender, birth_date) "
                #    "VALUES (%s, %s, %s, %s, %s)")
    # if cursor.execute(""" select * from containers_registered  """):
    if cursor.execute(""" select * from containers_registered """):
        alive = False
    else:
        print("alive is: ", alive)
        for (id, weight, unit) in cursor:
            print(id, weight, unit)
    cursor.close()

    cnx.close()
    return alive
