import os
import glob
import json
import time
import configure
from image_classifier import ImageClassifier


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Batch classifier', prog='Citizen Sensor')
    parser.add_argument('-d', '--directory', help='Path to the directory with images', required=True)
    args = parser.parse_args()

    start = time.time()
    config = configure.read_config()
    classifier = ImageClassifier(config)
    for filename in glob.glob(os.path.join(args.directory, '*.jpg')):
        print('Processing: {}'.format(filename))
        result = classifier.identify_image(filename)
        with open(result['filename'] + '.json', 'w') as f:
            res = json.dump(result, f, sort_keys=True, indent=4, separators=(',', ': '))
    print('Total time: {}'.format(time.time() - start))