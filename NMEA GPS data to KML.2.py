#!/usr/bin/python
#
# Converts GPS NMEA data into a Google earth KML file
#
# Copyright 2001 Ben Buxton. BSD Licensed.

import sys

# How many samples to integrate into 1
INTERVAL = 10
# Only use samples where this many satellites were visible.
NUM_SATS = 5

class Nmea(object):
  """"NMEA Data."""
  def __init__(self):
    self.sentences = []

  def Add(self, line):
    try:
      if line.startswith('$GPGGA'):
        sentence = Gpgga(line)
      elif line.startswith('$GPVTG'):
        sentence = Gpvtg(line)
      else:
        return
      self.sentences.append(sentence)
    except ValueError, e:
      pass


class Gpvtg(object):
  def __init__(self, data):
    """Constructor"""
    self.data = data
    self._Parse()

  def _Parse(self):
    fields, self.checksum = self.data.split('*')
    fields = fields.split(',')
    if len(fields) != 10:
      raise ValueError('Error parsing: %s' % self.data)

    # $GPVTG,77.12,T,,M,0.53,N,1.0,K,A*39
    (self.sentence, self.track_made_good, self.truenorth,
     _, _, self.knots, self.knot_units, self.kph,
     self.kph_units, self.sump) = fields

  def __str__(self):
    return "%s %s kph" % (self.data, self.kph)
    

class Gpgga(object):
  """A GPGGA Sentence."""
  def __init__(self, data):
    """Constructor."""
    self.data = data
    self._Parse()

  def _DegreeConvert(self, degrees):
    deg_min, dmin = degrees.split('.')
    degrees = int(deg_min[:-2])
    minutes = float('%s.%s' % (deg_min[-2:], dmin))
    decimal = degrees + (minutes/60)
    return decimal

  def _Parse(self):

    fields, self.checksum = self.data.split('*')
    fields = fields.split(',')
    if len(fields) != 15:
      raise ValueError('Error parsing: %s' % self.data)

    (self.sentence, self.fix_time, self.latitude, self.north_south,
     self.longitude, self.east_west, self.fix_quality,
     self.num_sats, self.horiz_dilution, self.altitude,
     self.altitude_units, self.geoid, self.geoid_units,
     self.update_time, self.gps_id) = fields

    if self.sentence != '$GPGGA':
      raise ValueError('Error parsing: %s' % self.data)

    self.latitude = self._DegreeConvert(self.latitude)
    self.longitude = self._DegreeConvert(self.longitude)

  def __str__(self):
    ret = ','.join((
        self.sentence, self.fix_time, self.latitude, self.north_south,
        self.longitude, self.east_west, self.fix_quality,
        self.num_sats, self.horiz_dilution, self.altitude,
        self.altitude_units, self.geoid, self.geoid_units,
        self.update_time, self.gps_id))
    ret += '*%s' % self.checksum
    return ret


class Kml(object):
  """A kml writer."""
  def __init__(self, name):
    self.data = []
    self.marks = 0
    self.Header(name)

  def Header(self, name):
    header = """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.2">
<Document>
<name>%s</name>

<Style id="icon1">
<IconStyle>
<scale>0.5</scale>
</IconStyle>
</Style>

<Style id="style1">
<LineStyle>
<color>ffffff00</color>
<colorMode>normal</colorMode>
<width>5</width>
</LineStyle>
</Style>

<Style id="color31">
<LineStyle>
<color>ffff2100</color>
<colorMode>normal</colorMode>
<width>3</width>
</LineStyle>
</Style>


<Folder>
<name>ash haunts</name>
<open>1</open>
""" % name
    self.data.append(header)

  def Placemark(self, gga, vtg):
    self.marks += 1
    if self.marks % INTERVAL:
      return False
    if gga.fix_quality != '1' or int(gga.num_sats) < NUM_SATS:
      return False
    timestamp = '%s:%s:%s' % (
        gga.fix_time[:2],
        gga.fix_time[2:4],
        gga.fix_time[4:])
    latitude = gga.latitude
    if gga.north_south == 'S':
      latitude = 0 - latitude

    longitude = gga.longitude
    if gga.east_west == 'W':
      longitude = 0 - longitude

    mark = """
<Placemark>
<name>%s (UTC), %s km/h</name>
<description>
Number of Satellites: %s</description>
<Point>
<coordinates>%f,%f,%s</coordinates>
</Point>
</Placemark>

""" % (timestamp, vtg.kph, gga.num_sats,
       longitude, latitude, gga.altitude)

    self.data.append(mark)
    return True

  def Tail(self):
    self.data.append("""
</Folder>
</Document>
</kml>
""")


  def StartLine(self):
    self.data.append ("""
</Folder>
<Folder>
<name>paths</name>
<open>0</open>
""")


  def Line(self, gga1, gga2):
    latitude1 = gga1.latitude
    if gga1.north_south == 'S':
      latitude1 = 0 - latitude1
    longitude1= gga1.longitude
    if gga1.east_west == 'W':
      longitude1 = 0 - longitude1

    latitude2 = gga2.latitude
    if gga2.north_south == 'S':
      latitude2 = 0 - latitude2
    longitude2= gga2.longitude
    if gga2.east_west == 'W':
      longitude2 = 0 - longitude2

    mark = """
<Placemark>
<name>line part</name>
<styleUrl>#color31</styleUrl>
<LineString>
<extrude>0</extrude>
<tessellate>1</tessellate>
<altitudeMode>clampToGround</altitudeMode>
<!-- kml:altitudeModeEnum: clampToGround, relativeToGround, or absolute -->
<coordinates>%s,%s,%s
%s,%s,%s
</coordinates></LineString></Placemark>
""" % (longitude1, latitude1, gga1.altitude,
       longitude2, latitude2, gga2.altitude)

    self.data.append(mark)

  def __str__(self):
    return '\n'.join(self.data)

nmea = Nmea()

if len(sys.argv) < 2:
  print 'Usage: %s <nmea_datafile>' % sys.argv[0]
  sys.exit(1)

fd = open(sys.argv[1])
for line in fd.readlines():
  line = line.strip()
  nmea.Add(line)

k = Kml(sys.argv[1])

placemarks = []
gga = vtg = None
for index, s in enumerate(nmea.sentences):
  if isinstance(s, Gpgga):
    gga = s
  elif isinstance(s, Gpvtg):
    vtg = s
    if gga and vtg:
      if k.Placemark(gga, vtg):
        placemarks.append(gga)
      gga = None

previous = None
k.StartLine()
for index, s in enumerate(placemarks):
  if not isinstance(s, Gpgga):
    continue

  if previous is None:
    previous = s
    continue

  k.Line(previous, s)
  previous = s
  

k.Tail()
print k
