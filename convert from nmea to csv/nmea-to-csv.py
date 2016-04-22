import csv
from datetime import datetime
import math
import sys
import time

# adapt this to your file
INPUT_FILENAME = sys.argv[1]
OUTPUT_FILENAME = "output.csv"


# open the input file in read mode
with open(INPUT_FILENAME, 'r') as input_file:

    # open the output file in write mode
    with open(OUTPUT_FILENAME, 'wt') as output_file:

        # create a csv reader object from the input file (nmea files are basically csv)
        reader = csv.reader(input_file)

        # create a csv writer object for the output file
        writer = csv.writer(output_file, delimiter=',', lineterminator='\n')

        # write the header line to the csv file
        writer.writerow(['date','time','speed', 'latitude','latitude direction' ,'longtitude','longtitude direction', 'fix', 'horizontal', 'altitude','altitude direction'])

        # iterate over all the rows in the nmea file
        date = None
        time = None
        for row in reader:

            # skip all lines that do not start with $GPRMC

            if row[0] in ("$GPRMC"):
                speed=row[7]
                date=row[9]
            if row[0] in ("$GPGGA", "$GPGLL"):

                # for each row, fetch the values from the row's columns
                # columns that are not used contain technical GPS stuff that you are probably not interested in

                time = row[1]
                latitude = row[2]
                latitude_direction = row[3]
                longtitude = row[4]
                longtitude_direction = row[5]
                fix=row[6]
                horizontal=row[7]
                altitude=row[8]
                altitude_direction=row[9]

            if (date is not None and time is not None):
                # merge the time and date columns into one Python datetime object (usually more convenient than having both separately)

                # merge the time and date columns into one Python datetime object (usually more convenient than having both separately)
                #date = datetime.strptime(date, '%d%m%y')

                # convert the Python datetime into your preferred string format, see http://www.tutorialspoint.com/python/time_strftime.htm for futher possibilities
                #date = date.strftime('%y-%m-%d')
                #time = datetime.strptime(time, '%H%M%S.%f')

                # convert the Python datetime into your preferred string format, see http://www.tutorialspoint.com/python/time_strftime.htm for futher possibilities
               # time = time.strftime('%H:%M:%S.%f')[       :-3]  # [:-3] cuts off the last three characters (trailing zeros from the fractional seconds)

                # convert the Python datetime into your preferred string format, see http://www.tutorialspoint.com/python/time_strftime.htm for futher possibilities

                # lat and lon values in the $GPRMC nmea sentences come in an rather uncommon format. for convenience, convert them into the commonly used decimal degree format which most applications can read.
                # the "high level" formula for conversion is: DDMM.MMMMM => DD + (YY.ZZZZ / 60), multiplicated with (-1) if direction is either South or West
                # the following reflects this formula in mathematical terms.
                # lat and lon have to be converted from string to float in order to do calculations with them.
                # you probably want the values rounded to 6 digits after the point for better readability.
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
                writer.writerow([date , time,speed, latitude,latitude_direction,longtitude,longtitude_direction, fix, horizontal, altitude,altitude_direction])
print "Done!"