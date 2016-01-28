#!/usr/bin/env python

from __future__ import division
from datetime import datetime

import exifread
from geopy.geocoders import Nominatim

"""
Grab these tags:

SceneCaptureType
SubjectDistance
SubjectDistanceRange
Orientation
ExposureProgram
SelfTimerMode
ApertureValue
LightSource
Flash
ShutterSpeedValue
"""



geolocator = Nominatim()

def convert_to_deg(degrees, minutes, seconds):
    if isinstance(degrees, tuple):
        degrees = rational_to_real(*degrees)
    if isinstance(minutes, tuple):
        minutes = rational_to_real(*minutes)
    if isinstance(seconds, tuple):
        seconds = rational_to_real(*seconds)
    return degrees + minutes / 60 + seconds / 3600

def rational_to_real(numerator, denominator=0):
    if denominator == 0:
        return numerator
    return numerator / denominator

def exif_dms_to_decimal_deg(gps_exif):
    latitude = gps_exif.get(piexif.GPSIFD.GPSLatitude)
    if latitude:
        latitude = convert_to_deg(*latitude)
        if gps_exif[piexif.GPSIFD.GPSLatitudeRef] == 'S':
            latitude *= -1
    else:
        return None

    longitude = gps_exif.get(piexif.GPSIFD.GPSLongitude)
    if longitude:
        longitude = convert_to_deg(*longitude)
        if gps_exif[piexif.GPSIFD.GPSLongitudeRef] == 'S':
            longitude *= -1
    else:
        return None

    return (latitude, longitude)
def gpsToString(coordinate):
 #   sec = rational_to_real(*map(int, str(coordinate[2]).split("/", 2)))
#    print coordinate[0].__class__
    return str(convert_to_deg((coordinate[0].num, coordinate[0].den), (coordinate[1].num, coordinate[1].den), (coordinate[2].num, coordinate[2].den)))



def get_gps_metadata(filepath, reverse_location=False):
    result = {}

    default_for_missing_values = 'Unknown'

#    try:
#        exif_dict = piexif.load(filepath)
#    except ValueError as ex:
#        result['Unknown'] = str(ex).replace('\n', ' ')
#        return result
#    except struct.error as ex:
#        print ex
#        result['Unknown'] = 'Internal error.'
#        return result
    file = open(filepath, 'rb')
    tags = exifread.process_file(file)

#    for tag in tags.keys():
#        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#            print "Key: %s, value %s" % (tag, tags[tag])

#    print 'tags'#    result['date'] = tags['date]


#    exif = exif_dict.get('Exif')
    if tags:
        date = tags['Image DateTime']
        try:
            result['date'] = str(datetime.strptime(date, '%Y:%m:%d %H:%M:%S').date()) if date else default_for_missing_values
        except:
            result['date'] = default_for_missing_values

        shutter = tags['EXIF ExposureTime'].values[0] if 'EXIF ExposureTime' in tags else default_for_missing_values
        result['ShutterSpeedValue'] = rational_to_real(shutter.num , shutter.den)
        scene_capture_type = tags['EXIF SceneCaptureType'] if 'EXIF SceneCaptureType' in tags else default_for_missing_values
        result['SceneCaptureType'] = scene_capture_type
        subject_distance = tags['EXIF SubjectDistance'] if 'EXIF SubjectDistance' in tags else default_for_missing_values
        result['SubjectDistance'] = subject_distance
        subject_distance_range = tags['EXIF SubjectDistanceRange'] if 'EXIF SubjectDistanceRange' in tags else default_for_missing_values
        result['SubjectDistanceRange'] = subject_distance_range
        aperture = tags['EXIF ApertureValue'].values[0] if 'EXIF ApertureValue' in tags else default_for_missing_values
        result['ApertureValue'] = rational_to_real(aperture.num, aperture.den)
        light_source = tags['EXIF LightSource'] if 'EXIF LightSource' in tags else default_for_missing_values   #unsure
        result['LightSource'] = light_source
        image_orientation = tags['Image Orientation'] if 'Image Orientation' in tags else default_for_missing_values
        result['Orientation'] = image_orientation

# GPS
        altitude = tags['GPS GPSAltitude'].values[0] if 'GPS GPSAltitude' in tags else default_for_missing_values
        result['altitude'] = rational_to_real(altitude.num, altitude.den) if type(altitude) != str else default_for_missing_values

        datum = tags['GPS GPSMapDatum'] if 'GPS GPSMapDatum' in tags else default_for_missing_values
        result['datum'] = datum

        latitude = tags['GPS GPSLatitude'].values if 'GPS GPSLatitude' in tags else 0
        longtitude = tags['GPS GPSLongitude'].values if 'GPS GPSLongitude'  in tags else 0
        position =  gpsToString(latitude) + ", " + gpsToString(longtitude)
        result['position'] = position 
#
        # if reverse_location and position:
        #      try:
        #          result['location'] = geolocator.reverse(position).address
        #      except Exception:
        #          result['location'] = default_for_missing_values
    return result

if __name__ == '__main__':
    import argparse
    import configure

    parser = argparse.ArgumentParser(description='GPS data parser', prog='Citizen Sensor')
    parser.add_argument('-i', '--image', help='Path to an image', type=configure.check_file_exist_argparse, required=True)
    args = parser.parse_args()
    metadata = get_gps_metadata(args.image, reverse_location=True)
    print (metadata)
