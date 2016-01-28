from __future__ import division
import boto
import boto.s3.connection
import cPickle as pickle
import os
import configure
from boto.s3.keyfile import KeyFile

def establish_connection_to_S3():
    config = configure.read_config()
    connection = boto.s3.connect_to_region(config['AWS']['region'],
       aws_access_key_id=config['AWS']['access_key_id'],
       aws_secret_access_key=config['AWS']['secret_key'],
       is_secure=True,
       calling_format = boto.s3.connection.OrdinaryCallingFormat())
    return connection


def check_if_loaded(f):
    def wrapper(*args):
        loaded = args[0].loaded
        if not loaded:
            raise BucketNotLoadedException('Load the data first - call load')
        return f(*args)
    return wrapper


class BucketWrapper(object):

    def __init__(self, bucket_name):
        self.name = bucket_name
        self.bucket = None
        self.size = 0
        self.count = 0
        self.keys = []
        self.loaded = False

    @check_if_loaded
    def download_all_from_bucket(self):
        for key in self.bucket:
            res = key.get_contents_to_filename(key)

    @check_if_loaded
    def get_bucket_info(self):
        return BucketInfo(name=self.bucket.name, size_in_bytes=self.size, count=self.count)

    def load(self):
        "Long-lasting operation"
        accepted_file_formats = ('.jpg', '.png')
        connection = establish_connection_to_S3()
        self.bucket = connection.get_bucket(self.name)

        pickled_bucket = self.name + '.pickle'
        if os.path.isfile(pickled_bucket) and os.access(pickled_bucket, os.R_OK):
            print('Loading pickled bucket')
            with open(pickled_bucket, 'rb') as file_with_bucket:
                self.keys = pickle.load(file_with_bucket)
        else:
            for key in self.bucket:
                if key.name.endswith(accepted_file_formats):
                    self.keys.append(key)
            print('Saving pickled bucket')
            with open(pickled_bucket, 'wb') as file_with_bucket:
                pickle.dump(self.keys, file_with_bucket, pickle.HIGHEST_PROTOCOL)

        self.loaded = True
        return self

    @check_if_loaded
    def pop(self, idx=0):
        return self.keys.pop(idx)

    def get_info(self):
        for key in self.bucket:
            self.size += key.size
        return BucketInfo(self.name, self.size, len(self.keys))


class BucketInfo(object):

    def __init__(self, name, size_in_bytes, count):
        self.size_in_bytes = size_in_bytes
        self.count = count
        self.name = name

    def __str__(self):
        return 'Bucket: {}, Size: {:.2f} MB, Count: {}'.format(self.name, self.size_in_bytes / 10**6, self.count)


class BucketNotLoadedException(Exception):
    "The data were not loaded into the bucket"


if __name__ == '__main__':
    import argparse
    import configure
    import json
    from image_classifier import ImageClassifier

    config = configure.read_config()

    parser = argparse.ArgumentParser(description='S3 Connector', prog='Citizen Sensor')
    parser.add_argument('-b', '--bucket', help='Bucket name on AWS S3', required=True)
    args = parser.parse_args()

    bucket = BucketWrapper(args.bucket).load()

    classifier = ImageClassifier(config)

    error_file = open('errors.log', 'w')

    while bucket.keys:
        try:
            key = bucket.pop()
            keyfile = KeyFile(key)
            print('Processing: {}'.format(keyfile.name))
            result = classifier.identify_image(keyfile)
            with open(result['filename'] + '.json', 'w') as f:
                res = json.dump(result, f, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as ex:
            try:
                error_file.write('Key: {} failed with error: {} \n'.format(key.name, str(ex)))
            except Exception as ex:
                error_file.write('Miserable failure: {} \n'.format(str(ex)))
    error_file.close()