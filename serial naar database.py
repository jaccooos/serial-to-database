import serial
import pymysql
import time

device = '/dev/ttyACM0'
baudrate = 9600

serial_arduino = serial.Serial(device, baudrate, timeout=1)


def execute_query(query):
    try:
        db_conn = pymysql.connect(host="localhost",
                                  user="monitor",
                                  passwd="Raspberry",
                                  db="projectbirra") or print("could not connect to database")
        db_cursor = db_conn.cursor()
        db_cursor.execute(query)
        db_conn.commit()
        db_cursor.close()
        db_conn.close()
    except Exception:
        print("Error while executing query")


def get_first_order(status):
    try:
        db_conn = pymysql.connect(host="localhost",
                                  user="monitor",
                                  passwd="Raspberry",
                                  db="projectbirra") or print("could not connect to database")
        db_cursor = db_conn.cursor()
        row_count = db_cursor.execute("SELECT idBestelling FROM bestelling WHERE Status = " + str(status) + " LIMIT 1")

        if row_count > 0: # If there are more then 0 rows
            row = db_cursor.fetchone()
            db_cursor.close()
            db_conn.close()
            return row[0]

        db_cursor.close()
        db_conn.close()
        return -1

    except Exception:
        print("Error while executing query")
        return -1


while True:
    # Wait for 1 second on data
    try:
        data = str(serial_arduino.readline(), 'ascii')
    except UnicodeDecodeError:
        data = ""
        print("Can't decode data")

    if len(data) > 0:
        print("Data received: ", data)

        if data[0] == "d":  # Done
            id_order = get_first_order(2)  # Pak eerste bestelling die bezig is
            if id_order != -1:
                execute_query("UPDATE bestelling SET Status=3 WHERE idBestelling=" + str(id_order))  
        
        elif data[0] == "e":  # Error
            execute_query("UPDATE Statussen SET Error=1, Bezig=0, Gereed=0")
            id_order = get_first_order(2)  # Pak eerste bestelling die bezig is
            if id_order != -1:
                execute_query("UPDATE bestelling SET Status=1 WHERE idBestelling=" + str(id_order))

        elif data[0] == "s":  # Standby
            status_nummer = data[1:]
			if status_nummer == 0
				id_order = get_first_order(1)  # Pak eerste verzonden bestelling in queue
				if id_order != -1:
					execute_query("UPDATE bestelling SET Status=2 WHERE idBestelling=" + str(id_order))
			elif status_nummer == 6
				execute_query("DELETE FROM bestelling")  # Verwijder alle bestellingen
			elif status_nummer < 8
                execute_query("UPDATE Statussen SET Status=" + status_nummer)
				execute_query("UPDATE Statussen SET Error=0, Bezig=1, Gereed=0")
            else 
                pass
        
        
        elif data[0] == "c":  # Celcius
            temperature = data[1:]
            execute_query("UPDATE Statussen SET Temperatuur=" + temperature)
			
		elif data[0] == "m":  # Celcius
            magazijn = data[1:]
            execute_query("UPDATE Statussen SET Magazijn=" + magazijn)
		
		elif data[0] == "v":  # Celcius
            vooraad = data[1:]
            execute_query("UPDATE Statussen SET Vooraad=" + vooraad)

    print("Checking database..")
    id_order = get_first_order(0)
    if id_order != -1:  # New order available
        print("Adding order", id_order, "to queue")
        serial_arduino.write('b'.encode())
        time.sleep(0.1)

        # Check if R received
        try:
            data = ""
            data = str(serial_arduino.readline(), 'ascii')

            if len(data) > 0 and data[0] == 'r':
                execute_query("UPDATE bestelling SET Status=1 WHERE idBestelling=" + str(id_order))
        except UnicodeDecodeError:
            data = ""
            print("Can't decode data")



