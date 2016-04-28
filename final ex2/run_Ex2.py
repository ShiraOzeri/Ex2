#!/usr/bin/python27
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
#tike the file_path from user
Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
file_path= filename
if(file_path ==""):
    sys.exit(0)
#connected to the data base
conn = sqlite3.connect('MyDb.db')
c = conn.cursor()
################################################imput to DB###########################################
#put the info to ouer data base
def f0():
    INPUT_FILENAME = file_path
    with open(INPUT_FILENAME, 'r') as input_file:
        reader = csv.reader(input_file)
        c.execute('DROP TABLE IF EXISTS info')
        #flag will tell us if the GPGGA is good if yes continue to the GPRMC
        flag = 0
        # Create table
        c.execute('''CREATE TABLE info
                         (date text,time text,speed float, latitude text, latitude_direction text, longitude text, longitude_direction text,fix text,horizontal_dilution text,altitude text)''')
        # create a csv reader object from the input file (nmea files are basically csv)
        date=None
        time=None
        flag = 0
        for row in reader:

            if row[0].startswith('$GPGGA'):

                if row[6] != '1':
                    fix = 0
                    time = 0
                    latitude = 0
                    latitude_direction = 0
                    longitude = 0
                    longtitude_direction = 0
                    horizontal = 0
                    altitude = 0
                else:
                    fix=1
                    time = float(row[1])
                    latitude = row[2]
                    latitude_direction = row[3]
                    longitude = row[4]
                    longtitude_direction = row[5]
                    horizontal = row[7]
                    altitude = row[9]
                    flag = 1
            elif row[0].startswith('$GPRMC'):
                speed = row[7]
                date = row[9]
                warning = row[2]
                if warning == 'V':
                    continue
            if date!=None and time!=None:
                 c.execute("INSERT INTO info VALUES (?,?,?,?,?,?,?,?,?,?)",(date,time,speed, latitude, latitude_direction, longitude, longtitude_direction,fix,horizontal,altitude))
            # Save (commit) the changes
                 conn.commit()
                 flag=0
                 date=None
                 time=None
    DBtoCSV()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    #conn.close()

#ans to Q1 return the path in spazipic ouer
def f1():
    def f1_1():
        def f1_2():
            def fe():
                root4.destroy()
            end_time = 0
            try:
                end_time = (float)(E2.get())
            except:
                print 'no enter a float number'
            c.execute('DELETE FROM info WHERE time>?', (end_time,))
            conn.commit()
            DBtoCSV()

            root3.destroy()
            root4 = Tk()
            root4.title("end time")
            root4.geometry("600x200")
            ButtonCSV = Button(root4, text="convert to csv", width=100, fg='red', font=16, command=DBtoCSV2)
            ButtonCSV.pack()

            ButtonKML = Button(root4, text="convert to kml", width=100, fg='red', font=16, command=DBtoKML)
            ButtonKML.pack()

            ButtonEXIT = Button(root4, text="exit", width=100, fg='red', font=16, command=fe)
            ButtonEXIT.pack()

        begin_time = 0
        try:
            begin_time = (float)(E1.get())
        except:
            print 'no enter a float number'
        c.execute('DELETE FROM info WHERE time<?', (begin_time,))
        conn.commit()

        root2.destroy()

        root3 = Tk()
        root3.title("end time")
        root3.geometry("600x200")

        E2 = Entry(root3, bd=5, fg="blue", width=20, background='pink')
        ButtonE2=Button(root3, text="enter a end time",width=100,fg='red',font=16)
        ButtonE2_1 = Button(root3, text="for example, if you want an hour- 23:40:01, type-234001", width=100, fg='red', font=14)

        Button1_2 = Button(root3, text="enter", command=f1_2, fg="blue", width=20, background='pink')
        ButtonE2.pack()
        ButtonE2_1.pack()
        E2.pack(side=LEFT)
        Button1_2.pack(side=RIGHT)


    root2 = Tk()
    root2.title("begin time")
    root2.geometry("600x200")

    E1 = Entry(root2, bd=5,fg="blue", width=20, background='pink')
    Button1_1 = Button(root2, text="enter", command=f1_1, fg="blue", width=20, background='pink')
    ButtonE1=Button(root2,text="enter a begin time",width=100,fg='red',font=16)
    ButtonE1_1 = Button(root2, text="for example, if you want an hour- 23:40:01, type-234001", width=100, fg='red',
                        font=14)

    ButtonE1.pack()
    ButtonE1_1.pack()
    E1.pack(side=LEFT)
    Button1_1.pack(side=RIGHT)

#return the ans to Q2 from the data base
def f2():
    c.execute('''SELECT horizontal_dilution text FROM info''')
    horizontal = c.fetchone()

    while True:
        if horizontal == None:
            break
        if (horizontal[0] != '0'):
            print horizontal[0]
            return
        else:
            horizontal = c.fetchall()
    print ('the file is not fix')
#return the ans to Q3 from the data base
def f3():
    def f3_1():
        def fe():
            root4.destroy()
        end_alt = 0
        try:
            end_alt = (float)(E1.get())
        except:
            print 'no enter a float number'
        root2.destroy()
        c.execute('DELETE FROM info WHERE altitude>?', (end_alt,))

        conn.commit()
        DBtoCSV()

        root4 = Tk()
        root4.title("end time")
        root4.geometry("600x200")
        ButtonCSV = Button(root4, text="convert to csv", width=100, fg='red', font=16, command=DBtoCSV2)
        ButtonCSV.pack()

        ButtonKML = Button(root4, text="convert to kml", width=100, fg='red', font=16, command=DBtoKML)
        ButtonKML.pack()

        ButtonEXIT = Button(root4, text="exit", width=100, fg='red', font=16, command=fe)
        ButtonEXIT.pack()

    root2 = Tk()
    root2.title("Question 3")
    root2.geometry("600x200")

    E1 = Entry(root2, bd=5, text="enter a altitude point", width=50, background='pink')
    ButtonE1 = Button(root2, text="enter a high altitude to Stop the route(above sea level)", width=100, fg='red', font=14)
    Button3_1 = Button(root2, text="enter", command=f3_1, fg="blue", width=20, background='pink')
    ButtonE1.pack()
    Button3_1.pack(side=LEFT)
    E1.pack(side=RIGHT)
#return the ans to Q4 from the data base
def f4():
    c.execute('''SELECT fix FROM info''')
    fix=c.fetchone()
    c.execute('''SELECT date text FROM info''')
    date=c.fetchone()
    i=0
    while True:
        if (date==None):
            break
        if (fix[i]=='1'):
            print (date[0])
            return
        else:
            date=c.fetchone()
    print('the file is not fix')

#return the ans to Q5 from the data base
def f5():
    fix = c.execute('''SELECT fix FROM info''')
    fix = c.fetchall()
    speed=c.execute('''SELECT speed float FROM info''')
    speed=c.fetchall()
    max=-1
    indexMax=0
    i=0
    for row in speed:
       if (fix[i]!=(u'0',)):
             if row>max:
                 max=row
                 indexMax=i
       i=i+1
    if (max==-1):
        print 'the file is not fix'
    else:
        print('the maximum speed is{0}'.format(speed[indexMax-1],type(speed[indexMax-1])))
#return the ans to Q6 from the data base
def f6():
    time=c.execute('''SELECT time text FROM info''')
    time=c.fetchone()
    first=0
    while True:
        if time==None:
            break
        if (first==0):
            first = (float)(time[0])
            time=c.fetchone()
        else:
            break

    last=first
    while True:
        if time == None:
            break
        if ( (float)(time[0])!= 0):
            last=(float)(time[0])
            time = c.fetchone()
        else:
            break
    if (first==0):
        print'the file is not fix'
    else:
        print (last-first)
   # print('the ruote time is', last-time)
#return the ans to Q7 from the data base
def f7():
    def f7_1():
        root2.destroy()
        time = c.execute('''SELECT time text FROM info''')
        time = c.fetchone()

        while True:
            if time == None:
                break
            if (time[0] != '0'):
                print(time[0])
                return
            else:
                time = c.fetchone()
        print 'the file is not fix'

    def f7_2():
        root2.destroy()
        time = c.execute('''SELECT time text FROM info''')
        time = c.fetchone()
        last = 0
        while True:
            if time == None:
                break
            if (time[0] != '0'):
                last = time[0]
                time = c.fetchone()
            else:
                time = c.fetchone()
        if (last != 0):
            print last
        else:
            print 'the file is not fix'

    root2 = Tk()
    root2.title("Question 7")
    root2.geometry("600x200")
    app2 = Frame(root2)
    app2.grid()

    Button7_1 = Button(app2, text="enter here if you want to get the begining of the routh", command=f7_1, fg="blue",
                        width=100,
                        background='pink')
    Button7_1.pack()
    Button7_2 = Button(app2, text="enter here if you want to get the end of the routh", command=f7_2, fg="blue",
                        width=100,
                        background='pink')

    Button7_2.pack()

#return the ans to Q8 from the data base
def f8():
    fix = c.execute('''SELECT fix FROM info''')
    fix = c.fetchall()
    i=0
    for row in fix:
        if (fix[i] == (u'1',)):
            print('the file is fix')
            return
        else:
            i=i+1
    print ('the file is not fix')

#return the ans to Q9 from the data base
def f9():
    def f9_1():
        def fe():
            root4.destroy()
        begin_lat=0
        try:
            begin_lat = (float)(E1.get())
        except:
            print 'no enter a float number'

        c.execute('DELETE FROM info WHERE latitude>?',(begin_lat,))

        conn.commit()
        DBtoCSV()
        root2.destroy()

        root4 = Tk()
        root4.title("end time")
        root4.geometry("600x200")
        ButtonCSV = Button(root4, text="convert to csv", width=100, fg='red', font=16, command=DBtoCSV2)
        ButtonCSV.pack()

        ButtonKML = Button(root4, text="convert to kml", width=100, fg='red', font=16, command=DBtoKML)
        ButtonKML.pack()

        ButtonEXIT = Button(root4, text="exit", width=100, fg='red', font=16, command=fe)
        ButtonEXIT.pack()

    root2 = Tk()
    root2.title("Question 9")
    root2.geometry("600x200")

    E1=Entry(root2,bd=5,width=50, background='pink')
    ButtonE1=Button(root2,text="enter a latitude point (for example-5920.7009)",font=14,fg='red')
    Button9_1 = Button(root2, text="enter", command=f9_1, fg="blue", width=20, background='pink')
    ButtonE1.pack()
    Button9_1.pack(side=LEFT)
    E1.pack(side=RIGHT)



#return the ans to Q10 from the data base
def f10():
    def f10_1():
        def fe():
            root4.destroy()

        begin_lon = 0
        try:
            begin_lon = (float)(E1.get())
        except:
            print 'no enter a float number'
        print begin_lon

        c.execute('DELETE FROM info WHERE latitude>?', (begin_lon,))

        conn.commit()
        DBtoCSV()
        root2.destroy()

        root4 = Tk()
        root4.title("end time")
        root4.geometry("600x200")
        ButtonCSV = Button(root4, text="convert to csv", width=100, fg='red', font=16, command=DBtoCSV2)
        ButtonCSV.pack()

        ButtonKML = Button(root4, text="convert to kml", width=100, fg='red', font=16, command=DBtoKML)
        ButtonKML.pack()

        ButtonEXIT = Button(root4, text="exit", width=100, fg='red', font=16, command=fe)
        ButtonEXIT.pack()

    root2 = Tk()
    root2.title("Question 10")
    root2.geometry("600x200")

    E1 = Entry(root2, bd=5, width=50, background='pink')
    ButtonE1 = Button(root2, text="enter a longitude point (for example-03455.30063)", font=14, fg='red')
    Button10_1 = Button(root2, text="enter", command=f10_1, fg="blue", width=20, background='pink')
    ButtonE1.pack()
    Button10_1.pack(side=LEFT)
    E1.pack(side=RIGHT)


    ###################################################################################
    # convert from the data base to csv file
def DBtoCSV():
    conn = sqlite3.connect("MyDb.db")  # open db
    cursor = conn.cursor()  # cursor to the db
    cursor.execute("select * from info;")  # execute a sql script

    with open("MyDB.csv", "wb") as csv_file:  # writing to csv
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # write headers
        csv_writer.writerows(cursor)
def DBtoCSV2():
    conn = sqlite3.connect("MyDb.db")  # open db
    cursor = conn.cursor()  # cursor to the db
    cursor.execute("select * from info;")  # execute a sql script

    with open(file_path+".csv", "wb") as csv_file:  # writing to csv
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([i[0] for i in cursor.description])  # write headers
        csv_writer.writerows(cursor)

# convert from the data base to kml file
def DBtoKML():
    skip = 5
    database = sqlite3.connect("MyDb.db")
    pois = database.execute("SELECT * FROM info;")
    file = str(file_path) + '.kml'
    FILE = open(file, 'w')
    FILE.truncate(0)
    FILE.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
    FILE.write('<kml xmlns="http://earth.google.com/kml/2.0">\n')
    FILE.write('    <Document>\n')
    FILE.write('     <Folder>\n')
    FILE.write('     <name>Point Features</name>\n')
    FILE.write('     <description>Point Features</description>\n\n')
    j = 0
    for poi in pois:
        if j % skip == 0:
            FILE.write('<Placemark>\n')
            FILE.write('    <TimeStamp>\n')
            FILE.write('     <when>%s%s</when>\n' % (poi[0], poi[1]))
            FILE.write('    </TimeStamp>\n')
            lat = float(poi[3][:2]) + (float(poi[3][2:]) / 60)
            lon = float(poi[5][:3]) + (float(poi[5][3:]) / 60)
            FILE.write('    <description><![CDATA[Lat: %s <br> Lon: %s<br> Speed: %s <br>]]></description>\n' % (
                lat, lon, (poi[2])))
            FILE.write('    <Point>\n')

            FILE.write('        <coordinates>%s,%s,%s</coordinates>\n' % (str(lon), str(lat), poi[9]))
            FILE.write('    </Point>\n')
            FILE.write('</Placemark>\n')
            j = j + 1
        else:
            j = j + 1
    FILE.write('        </Folder>\n')
    FILE.write('    </Document>\n')
    FILE.write('</kml>\n')
    FILE.close()
    database.close()
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
# convert from nmea to kml file
def conKML():
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
def conCSV():
    input_file = open(file_path, 'r')
    output_file = open(file_path + '.csv', 'w')
    reader = csv.reader(input_file)
    writer = csv.writer(output_file, delimiter=',', lineterminator='\n')

    # write the header line to the csv file
    writer.writerow(
        ['date', 'time', 'speed', 'latitude', 'latitude direction', 'longtitude', 'longtitude direction', 'fix',
         'horizontal', 'altitude'])

    # iterate over all the rows in the nmea file
    date = None
    time = None
    flag = 0
    for row in reader:

        if row[0].startswith('$GPGGA'):

            if row[6] != '1':
                fix = row[6]
                time = 0
                latitude = 0
                latitude_direction = 0
                longtitude = 0
                longtitude_direction = 0
                horizontal = 0
                altitude = 0
            else:
                time = float(row[1])
                latitude = row[2]
                latitude_direction = row[3]
                longtitude = row[4]
                longtitude_direction = row[5]
                horizontal = row[7]
                altitude = row[9]
                flag = 1
                fix=row[6]
        elif row[0].startswith('$GPRMC'):
            speed = row[7]
            date = row[9]
            warning = row[2]
            if warning == 'V':
                continue
        if date != None and time != None:

            if latitude_direction == 'S':
                latitude = latitude * -1

            if longtitude_direction == 'W':
                longtitude = longtitude * -1

            # write the calculated/formatted values of the row that we just read into the csv file
            writer.writerow(
                [date, time, speed, latitude, latitude_direction, longtitude, longtitude_direction, fix,
                 horizontal, altitude])

    input_file.close()
    output_file.close()

######################################################################################
#the gui this make the munu on ouer system
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
ButtonConKML = Button(app , text = "Make a kml file", command = conKML())
ButtonConKML.pack()
ButtonConCSV = Button(app , text = "Make a CSV file", command = conCSV())
ButtonConCSV.pack()
Button0000 = Button(app, text="")
Button0000.pack()
##############################################################################################
#here this is all the buttons on the system
#
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

Button7 = Button(app , text = "7.  Return time of beginning/end of routeh" , command = f7,fg = "blue",width=100, background='white')
Button7.pack()

Button8 = Button(app , text = "8.Is the file working properly or not." , command = f8,fg = "blue",width=100, background='white')
Button8.pack()

Button9 = Button(app , text = "9.Erase all the marks in a specified latitude" , command = f9,fg = "blue",width=100, background='white')
Button9.pack()

Button10 = Button(app, text="10.Erase all the marks in a specified longitude", command=f10, fg="blue", width=100, background='white')
Button10.pack()





mainloop()


##################################################################################################
