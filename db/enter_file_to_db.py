import MySQLdb
import pynmea2

###F1
#CREATE DATABASE Ex2DB;
db1 = MySQLdb.connect(host="localhost", user="erez", passwd="1234", nameDb="Ex2DB")
#create_database(db1.cursor())

def build_database():
    db1 = MySQLdb.connect(host="localhost", user="erez", passwd="1234",nameDb="Ex2DB")
    sql = db1.cursor()
    sql.execute("SET sql_notes = 0; ")
    CREATE_DATABASE = 'CREATE DATABASE Ex2DB'
    sql.execute(CREATE_DATABASE)

    #maby need double?
    #have more cols? shirle need to do the Q
    CREATE_TABLE = '''create table IF NOT EXISTS MainTable (
      full_nmea varchar(200) primary key ,
      latitude float(10),
      longitude float(10),
      height float(10),
      speed float(10),
      number of satellites int (5),
      time varchar(10),
           )
           '''
    sql.execute(CREATE_TABLE)


def put_nmea_to_db(s):
    db1 = MySQLdb.connect(host="localhost", user="erez", passwd="1234")
    sql = db1.cursor()
    msg = pynmea2.parse(s)
    time =  msg.time
    ##...



build_database()
put_nmea_to_db("$GPGGA,184353.07,1929.045,S,02410.506,E,1,04,2.6,100.00,M,-33.9,M,,0000*6D")