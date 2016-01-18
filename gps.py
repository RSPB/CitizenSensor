#!/usr/bin/env python

from __future__ import division
import exifread
from datetime import datetime
from geopy.geocoders import Nominatim


geolocator = Nominatim()

def _convert_to_deg(value):
    degrees = value[0].num / value[0].den
    minutes = value[1].num / value[1].den
    seconds = value[2].num / value[2].den
    return degrees + minutes / 60.0 + seconds / 3600.0


def get_gps_metadata(filepath, reverse_location=False):
    result = {}

    try:
        f = open(filepath, 'rb')
        tags = exifread.process_file(f)
        GPSDate = tags['GPS GPSDate'].values
        date = datetime.strptime(GPSDate, '%Y:%m:%d')

        GPSAltitude = tags['GPS GPSAltitude'].values
        altitude = eval(str(GPSAltitude[0]))

        GPSLatitude = tags['GPS GPSLatitude'].values
        GPSLatitudeRef = tags['GPS GPSLatitudeRef'].values
        latitude = _convert_to_deg(GPSLatitude) if GPSLatitudeRef == 'N' else -_convert_to_deg(GPSLatitude)

        GPSLongitude = tags['GPS GPSLongitude'].values
        GPSLongitudeRef = tags['GPS GPSLongitudeRef'].values
        longitude = _convert_to_deg(GPSLongitude) if GPSLongitudeRef == 'E' else -_convert_to_deg(GPSLongitude)

        GPSMapDatum = tags['GPS GPSMapDatum'].values

        result['coordinates'] = (latitude, longitude)
        result['altitude'] = altitude
        result['location'] = geolocator.reverse((latitude, longitude)).address if reverse_location else ''
        result['datum'] = GPSMapDatum
        result['date'] = str(date.date())
    except:
        result['coordinates'] = 'Unknown'
        result['altitude'] = 'Unknown'
        result['location'] = 'Unknown'
        result['datum'] = 'Unknown'
        try:
            result['date'] = tags['EXIF DateTimeOriginal'].values if 'EXIF DateTimeOriginal' in tags else 'Unknown'
        except:
            result['date'] = 'Unknown'

    return result

if __name__ == '__main__':
    import argparse
    import configure

    parser = argparse.ArgumentParser(description='GPS data parser', prog='Citizen Sensor')
    parser.add_argument('-i', '--image', help='Path to an image', type=configure.check_file_exist_argparse, required=True)
    args = parser.parse_args()
    metadata = get_gps_metadata(args.image, reverse_location=True)
    print metadata
