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
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
       )
    return connection


class Bucket(object):

    def __init__(self, bucket_name):
        connection = establish_connection_to_S3()
        self.bucket = connection.get_bucket(bucket_name)

    def download_all_from_bucket(self):
        for key in self.bucket:
            res = key.get_contents_to_filename(key)

    def get_bucket_info(self):
        total_bytes = 0
        total_files = 0
        for key in self.bucket:
            total_bytes += key.size
            total_files += 1
        return BucketInfo(size_in_bytes=total_bytes, count=total_files)


class BucketInfo(object):

    def __init__(self, size_in_bytes, count):
        self.size_in_bytes = size_in_bytes
        self.count = count

    def __str__(self):
        return 'Size: {:.2f} MB, Count: {}'.format(self.size_in_bytes / 10**6, self.count)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='S3 Connector', prog='Citizen Sensor')
    parser.add_argument('-b', '--bucket', help='Bucket name on AWS S3', required=True)
    args = parser.parse_args()

    bucket = Bucket(args.bucket)
    info = bucket.get_bucket_info()
    print(info)