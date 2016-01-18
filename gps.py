#!/usr/bin/env python

from __future__ import division
import piexif
from datetime import datetime
from geopy.geocoders import Nominatim


geolocator = Nominatim()

def _convert_to_deg(deg, min, sec):
    degrees = _rational_to_real(*deg)
    minutes = _rational_to_real(*min)
    seconds = _rational_to_real(*sec)
    return degrees + minutes / 60 + seconds / 3600

def _rational_to_real(numerator, denominator):
    return numerator / denominator

def dms_to_decimal_deg(gps_exif):
    latitude = gps_exif.get(piexif.GPSIFD.GPSLatitude)
    if latitude:
        latitude = _convert_to_deg(*latitude)
        if gps_exif[piexif.GPSIFD.GPSLatitudeRef] == 'S':
            latitude *= -1
    else:
        return None

    longitude = gps_exif.get(piexif.GPSIFD.GPSLongitude)
    if longitude:
        longitude = _convert_to_deg(*longitude)
        if gps_exif[piexif.GPSIFD.GPSLongitudeRef] == 'S':
            longitude *= -1
    else:
        return None

    return (latitude, longitude)


def get_gps_metadata(filepath, reverse_location=False):
    result = {}

    default = 'Unknown'
    exif_dict = piexif.load(filepath)

    if exif_dict['Exif']:
        date = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        result['date'] = str(datetime.strptime(date, '%Y:%m:%d %H:%M:%S').date()) if date else default

    if exif_dict['GPS']:
        altitude = exif_dict['GPS'].get(piexif.GPSIFD.GPSAltitude)
        result['altitude'] = int(_rational_to_real(*altitude)) if altitude else default

        datum = exif_dict['GPS'].get(piexif.GPSIFD.GPSMapDatum)
        result['datum'] = datum or default

        position = dms_to_decimal_deg(exif_dict['GPS'])
        result['position'] = position or default

        if reverse_location and position:
            result['location'] = geolocator.reverse(position).address

    return result

if __name__ == '__main__':
    import argparse
    import configure

    parser = argparse.ArgumentParser(description='GPS data parser', prog='Citizen Sensor')
    parser.add_argument('-i', '--image', help='Path to an image', type=configure.check_file_exist_argparse, required=True)
    args = parser.parse_args()
    metadata = get_gps_metadata(args.image, reverse_location=True)
    print metadata
