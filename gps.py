#!/usr/bin/env python

from __future__ import division
from datetime import datetime

import exifread
import exifread.utils
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
        if gps_exif[piexif.GPSIFD.GPSLongitudeRef] == 'W':
            longitude *= -1
    else:
        return None

    return (latitude, longitude)

def gpsToFloat(coordinate):
    return convert_to_deg((coordinate[0].num, coordinate[0].den), (coordinate[1].num, coordinate[1].den), (coordinate[2].num, coordinate[2].den))

def get_gps_metadata(filepath, reverse_location=False):
    result = {}

    default_for_missing_values = 'Unknown'

    file = open(filepath, 'rb')
    tags = exifread.process_file(file)
#   for tag in tags.keys():
#        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
#            print "Key: %s, value %s" % (tag, tags[tag])
    if tags:
        date = tags['Image DateTime'] if 'Image DateTime' in tags else default_for_missing_values
        print "##%s##" % (date)
        try:
            result['date'] = str(datetime.strptime(str(date), '%Y:%m:%d %H:%M:%S').date())
        except:
            result['date'] = default_for_missing_values
        shutter = tags['EXIF ExposureTime'].values[0] if 'EXIF ExposureTime' in tags else default_for_missing_values
        scene_capture_type = tags['EXIF SceneCaptureType'] if 'EXIF SceneCaptureType' in tags else default_for_missing_values
        subject_distance = tags['EXIF SubjectDistance'] if 'EXIF SubjectDistance' in tags else default_for_missing_values
        subject_distance_range = tags['EXIF SubjectDistanceRange'] if 'EXIF SubjectDistanceRange' in tags else default_for_missing_values
        aperture = tags['EXIF ApertureValue'].values[0] if 'EXIF ApertureValue' in tags else default_for_missing_values
        light_source = tags['EXIF LightSource'] if 'EXIF LightSource' in tags else default_for_missing_values   #unsure
        image_orientation = tags['Image Orientation'] if 'Image Orientation' in tags else default_for_missing_values
# GPS
        altitude = tags['GPS GPSAltitude'].values[0] if 'GPS GPSAltitude' in tags else default_for_missing_values
        datum = tags['GPS GPSMapDatum'] if 'GPS GPSMapDatum' in tags else default_for_missing_values
        latitude = tags['GPS GPSLatitude'].values if 'GPS GPSLatitude' in tags else 0
        longtitude = tags['GPS GPSLongitude'].values if 'GPS GPSLongitude'  in tags else 0

        position =  (gpsToFloat(latitude), gpsToFloat(longtitude)) if type(longtitude)!=int and type(latitude)!=int else default_for_missing_values
        result['ShutterSpeedValue'] = rational_to_real(shutter.num , shutter.den)
        result['SceneCaptureType'] = str(scene_capture_type)
        result['SubjectDistance'] = subject_distance
        result['SubjectDistanceRange'] = str(subject_distance_range)
        result['ApertureValue'] = rational_to_real(aperture.num, aperture.den)
        result['LightSource'] = str(light_source)
        result['Orientation'] = str(image_orientation)
        result['datum'] = str(datum)

        result['altitude'] = int(rational_to_real(altitude.num, altitude.den)) if type(altitude) != str else default_for_missing_values
        result['position'] = position

        if reverse_location and position:
             try:
                 result['location'] = geolocator.reverse(position).address
             except Exception:
                 result['location'] = default_for_missing_values
    return result

if __name__ == '__main__':
    import argparse
    import configure

    parser = argparse.ArgumentParser(description='GPS data parser', prog='Citizen Sensor')
    parser.add_argument('-i', '--image', help='Path to an image', type=configure.check_file_exist_argparse, required=True)
    args = parser.parse_args()
    metadata = get_gps_metadata(args.image, reverse_location=True)
    print metadata
