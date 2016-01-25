#!/usr/bin/env python

from __future__ import division
import piexif
from datetime import datetime
from geopy.geocoders import Nominatim


geolocator = Nominatim()

def convert_to_deg(degrees, minutes, seconds):
    if isinstance(degrees, tuple):
        degrees = rational_to_real(*degrees)
    if isinstance(minutes, tuple):
        minutes = rational_to_real(*minutes)
    if isinstance(seconds, tuple):
        seconds = rational_to_real(*seconds)
    return degrees + minutes / 60 + seconds / 3600

def rational_to_real(numerator, denominator):
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


def get_gps_metadata(filepath, reverse_location=False):
    result = {}

    default_for_missing_values = 'Unknown'
    exif_dict = piexif.load(filepath)

    if exif_dict['Exif']:
        date = exif_dict['Exif'].get(piexif.ExifIFD.DateTimeOriginal)
        try:
            result['date'] = str(datetime.strptime(date, '%Y:%m:%d %H:%M:%S').date()) if date else default_for_missing_values
        except:
            result['date'] = default_for_missing_values

    if exif_dict['GPS']:
        altitude = exif_dict['GPS'].get(piexif.GPSIFD.GPSAltitude)
        result['altitude'] = int(rational_to_real(*altitude)) if altitude else default_for_missing_values

        datum = exif_dict['GPS'].get(piexif.GPSIFD.GPSMapDatum)
        result['datum'] = datum or default_for_missing_values

        position = exif_dms_to_decimal_deg(exif_dict['GPS'])
        result['position'] = position or default_for_missing_values

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
