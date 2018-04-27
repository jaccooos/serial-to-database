
import serial 
import MySQLdb
import time

# 'sql7.freesqldatabase.com','sql7234794','xQ8u9lhzpC','sql7234794','3306'


dbConn = MySQLdb.connect(host=","root","root","testing") or die ("could not connect to database")
cursor = dbConn.cursor()
device = '/dev/ttyUSB0'
max=30
start=time.time()
while True:
    try:
        print "Trying...",device 
        arduino = serial.Serial(device, 9600) 
    except: 
        print "Failed to connect on",device    

    try: 
        data = arduino.readline()  
        if (data = "E")
		{
			try:
            cursor.execute("INSERT INTO Statussen (Error) VALUES (%s)", (true)
            dbConn.commit() 
            cursor.close()  
			except MySQLdb.IntegrityError:
			print "failed to insert data"
		}
		elif (data = "M")
		{ 
			# lees vervolgens het getal uit 
			
			try:
            cursor.execute("INSERT INTO Statussen (Magazijn) VALUES (%s)", (getal)
            dbConn.commit() 
            cursor.close()  
			except MySQLdb.IntegrityError:
			print "failed to insert data"
		}
		pieces = data.split("\t")  
		
        
        #finally:
            #cursor.close()
    except:
        print "Failed to get data from Arduino!"
    time.sleep(10)
    print "looping..."
    remaining=max+start-time.time()
    print "%s seconds remaining" % int(remaining)
    if remaining<=0:
        cursor.close()
        break