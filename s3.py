from __future__ import division
import boto
import boto.s3.connection
import configure


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
        self.files = []
        self.size = 0
        self.count = 0
        self.loaded = False

    @check_if_loaded
    def download_all_from_bucket(self):
        for key in self.bucket:
            res = key.get_contents_to_filename(key)

    @check_if_loaded
    def get_bucket_info(self):
        return BucketInfo(name=self.bucket.name, size_in_bytes=self.size, count=self.count)

    def load(self):
        "Long-lasting operation on large buckets"
        connection = establish_connection_to_S3()
        self.bucket = connection.get_bucket(self.name)
        for key in self.bucket:
            self.size += key.size
            self.count += 1
            self.files.append(key.name)
        self.loaded = True
        return self


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
    parser = argparse.ArgumentParser(description='S3 Connector', prog='Citizen Sensor')
    parser.add_argument('-b', '--bucket', help='Bucket name on AWS S3', required=True)
    args = parser.parse_args()

    bucket = BucketWrapper(args.bucket).load()
    info = bucket.get_bucket_info()
    print(info)