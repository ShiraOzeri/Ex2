from Tkinter import *
from Tkinter import Tk
import os, string, sys
from tkFileDialog import askopenfilename
import csv
import sqlite3
import math
import serial
import nmeagram
import time
from datetime import datetime
####################################################################################
file_path = ""
####################################################################################
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
file_path= filename
if(file_path ==""):
    sys.exit(0)
conn = sqlite3.connect('MyDb.db')
c = conn.cursor()
################################################imput to DB###########################################
def f0():
    INPUT_FILENAME = file_path
    with open(INPUT_FILENAME, 'r') as input_file:
        reader = csv.reader(input_file)
        c.execute('DROP TABLE IF EXISTS info')
        #flag will tell us if the GPGGA is good if yes continue to the GPRMC
        flag = 0
        # Create table
        c.execute('''CREATE TABLE info
                         (date text,time text,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text,direct_of_altitude text,altitude_location text)''')
        # create a csv reader object from the input file (nmea files are basically csv)
        for row in reader:
            # skip all lines that do not start with $GPGGA
            if not row:
                continue
            elif row[0].startswith('$GPGGA') and row[6]=='1':
                time= row[1]
                latitude = row[2]
                lat_direction = row[3]
                longitude = row[4]
                lon_direction = row[5]
                fix = row[6]
                horizontal = row[7]
                altitude = row[8]
                direct_altitude = row[9]
                altitude_location = row[10]
                flag = 1
            elif row[0].startswith('$GPRMC') and flag==1:
                speed = row[7]
                date = row[9]
                warning = row[2]
                if warning == 'V':
                    continue
                c.execute("INSERT INTO info VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",(date,time,speed, latitude, lat_direction, longitude, lon_direction,fix,horizontal,altitude,direct_altitude,altitude_location))
            # Save (commit) the changes
                conn.commit()
                flag=0
            else:
                continue
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    #conn.close()


def f1():
    print 1

def f2():
    print 2

def f3():
    print 3

def f4():
    c.execute('''SELECT date text FROM info''')
    date=c.fetchone()
    print ('the date is {0}'.format(date[0], type(date[0])))


def f5():
    speed=c.execute('''SELECT speed float FROM info''')
    max=0
    for row in speed:
        if row>max:
            max=row
    print('the maximum speed is',max)

def f6():
    time=c.execute('''SELECT time text FROM info''')
    last=0
    for row in time:
        last=row
        print last
   # print('the ruote time is', last.time)

def f7():
   print 7

def f8():
    print 8

def f9():
    print 9

def f10():
     print 10

def f11():
    print 11

def f12():
     print 12

####################################################################################
#con
def nmeaFileToCoords(f):
    """Read a file full of NMEA sentences and return a string of lat/lon/z
    coordinates.  'z' is often 0.
    """
    data = []
    for line in f.readlines():
        if line[:6] in ("$GPGGA", "$GPGLL"):
            nmeagram.parseLine(line)
            data.append(str(nmeagram.getField("Longitude")))
            data.append(",")
            data.append(str(nmeagram.getField("Latitude")))
            data.append(",0 ")
    return string.join(data, '')

def conKML(file_path):
    KML_EXT = ".kml"

    KML_TEMPLATE = \
        """<?xml version="1.0" encoding="UTF-8"?>
        <kml xmlns="http://earth.google.com/kml/2.0">
        <Document>
          <name>NMEA to KML: %s</name>
          <Style id="dwhStyle000">
            <LineStyle id="dwhLineStyleRed6">
              <color>7f0000ff</color>
              <width>6</width>
            </LineStyle>
          </Style>
          <Placemark>
            <name>%s</name>
            <styleUrl>#dwhStyle000</styleUrl>
            <MultiGeometry>
              <LineString>
                <coordinates>
                %s
                </coordinates>
              </LineString>
            </MultiGeometry>
          </Placemark>
        </Document>
        </kml>
        """

    fn = file_path
    assert os.path.exists(fn)

    # Create the KML output file
    fo = open(fn + KML_EXT, 'w')
    fi = open(fn, 'r')
    fo.write(KML_TEMPLATE % (fn, fn, nmeaFileToCoords(fi)))
    fi.close()
    fo.close()

def conCSV(file_path):
    input_file = open(file_path, 'r')
    output_file = open(file_path + '.csv', 'w')
    reader = csv.reader(input_file)
    writer = csv.writer(output_file, delimiter=',', lineterminator='\n')

    # write the header line to the csv file
    writer.writerow(
        ['date', 'time', 'speed', 'latitude', 'latitude direction', 'longtitude', 'longtitude direction', 'fix',
         'horizontal', 'altitude', 'altitude direction'])

    # iterate over all the rows in the nmea file
    date = None
    time = None
    for row in reader:

        # skip all lines that do not start with $GPRMC

        if row[0] in ("$GPRMC"):

            warning = row[2]
            if warning == 'V':
                continue
            speed = row[7]
            date = row[9]

        if row[0] in ("$GPGGA", "$GPGLL"):
            time = row[1]
            latitude = row[2]
            latitude_direction = row[3]
            longtitude = row[4]
            longtitude_direction = row[5]
            fix = row[6]
            horizontal = row[7]
            altitude = row[8]
            altitude_direction = row[9]

        if (date is not None and time is not None):

            latitude = round(math.floor(float(latitude) / 100) + (float(latitude) % 100) / 60, 6)
            if latitude_direction == 'S':
                latitude = latitude * -1

            longtitude = round(math.floor(float(longtitude) / 100) + (float(longtitude) % 100) / 60, 6)
            if longtitude_direction == 'W':
                longtitude = longtitude * -1

            # speed is given in knots, you'll probably rather want it in km/h and rounded to full integer values.
            # speed has to be converted from string to float first in order to do calculations with it.
            # conversion to int is to get rid of the tailing ".0".
            speed = int(round(float(speed) * 1.852, 0))

            # write the calculated/formatted values of the row that we just read into the csv file
            writer.writerow(
                [date, time, speed, latitude, latitude_direction, longtitude, longtitude_direction, fix,
                 horizontal, altitude, altitude_direction])
    input_file.close()
    output_file.close()


######################################################################################
root = Tk()
root.title("Ex2")
root.geometry("800x600")
app = Frame(root)
app.grid()
##
Button0 = Button(app , text = "Hello to you! Welcome to EX2" ,fg = "red",width=100, background='black',height=10 )
Button0.pack()

Button00 = Button(app , text = "Upload the file to Data Base! it will take a few seconds! **clike me to start!** " ,fg = "black",width=100, background='red', command = f0 )
Button00.pack()

Button000 = Button(app , text = ""  )
Button000.pack()
ButtonConKML = Button(app , text = "Make a kml file", command = conKML(file_path)  )
ButtonConKML.pack()
ButtonConCSV = Button(app , text = "Make a CSV file", command = conCSV(file_path)  )
ButtonConCSV.pack()
Button0000 = Button(app, text="")
Button0000.pack()
##############################################################################################
Button1 = Button(app , text = "1.Creating a new route between specific hours" , command = f1,fg = "blue",width=100, background='white')
Button1.pack()

Button2 = Button(app , text = "2. Return a number of satellites that operated" , command = f2,fg = "blue",width=100, background='white')
Button2.pack()

Button3 = Button(app , text = "3. Stop a route if passing maximum speed/maximum height (above sea level)." , command = f3,fg = "blue",width=100, background='white')
Button3.pack()

Button4 = Button(app , text = "4.Return date line (GPRMC)." , command = f4,fg = "blue",width=100, background='white')
Button4.pack()

Button5 = Button(app , text = "5. Maximum speed above ground." , command = f5,fg = "blue",width=100, background='white')
Button5.pack()

Button6 = Button(app , text = "6. Return route time." , command = f6,fg = "blue",width=100, background='white')
Button6.pack()

Button7 = Button(app , text = "7. Return route length" , command = f7,fg = "blue",width=100, background='white')
Button7.pack()

Button8 = Button(app , text = "8.Is the file working properly or not." , command = f8,fg = "blue",width=100, background='white')
Button8.pack()

Button9 = Button(app , text = "9.Erase all the marks in a specified longitude" , command = f9,fg = "blue",width=100, background='white')
Button9.pack()

Button10 = Button(app, text="10.Erase all the marks in a specified latitude", command=f10, fg="blue", width=100, background='white')
Button10.pack()

Button11 = Button(app , text = "11.Format of place recognition (DGPS/GPS/ERROR)." , command = f11,fg = "blue",width=100, background='white')
Button11.pack()

Button12 = Button(app , text = "12. Return time of beginning/end of routeh" , command = f12,fg = "blue",width=100, background='white')
Button12.pack()

mainloop()


##################################################################################################
