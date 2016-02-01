import os
import glob
import json
import pandas as pd
import time
import configure
from image_classifier import ImageClassifier
from writer import Writer


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Batch classifier', prog='Citizen Sensor')
    parser.add_argument('-d', '--directory', help='Path to the directory with images', required=True)
    parser.add_argument('-o', '--output', help='Output filename', required=True)
    args = parser.parse_args()

    start = time.time()
    config = configure.read_config()
    classifier = ImageClassifier(config)
    writer = Writer(config, args.output)
    writer.write_headers()
    for filename in glob.glob(os.path.join(args.directory, '*.jpg')):
        print('Processing: {}'.format(filename))
        with open(filename, 'rb') as f:
            result = classifier.get_prediction(f)
        writer.write(result)
    print('Total time: {}'.format(time.time() - start))