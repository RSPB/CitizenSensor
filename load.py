import boto
import boto.s3.connection
import configure


bucket = 'citizen-mapping-test'
config = configure.read_config()

conn = boto.s3.connect_to_region(config['AWS']['region'],
       aws_access_key_id=config['AWS']['access_key_id'],
       aws_secret_access_key=config['AWS']['secret_key'],
       is_secure=True,
       calling_format = boto.s3.connection.OrdinaryCallingFormat(),
       )

bucket = conn.get_bucket(bucket)
for key in bucket.list():
    try:
        print(key)
        # res = key.get_contents_to_filename(key.name)
    except Exception, e:
        print(e.msg)