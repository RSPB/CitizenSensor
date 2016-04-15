import os
import glob2
import argparse
import time
import configure
from image_classifier import ImageClassifier
from writer import Writer


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Batch classifier', prog='Citizen Sensor')
    parser.add_argument('-d', '--directory', help='Path to the directory with images', required=True)
    parser.add_argument('-o', '--output', help='Output file name', default=None)
    parser.add_argument('-c', '--config', help='Path to the config file', default='config.ini')
    parser.add_argument('-x', '--extra', help='Path to a supplementary data set, organised as CSV, which contains '
        'key to join and values to be joined', default=None)
    parser.add_argument('-k', '--key', help='Index of column (counted from 0) in which the key is present. The key should '
        'be unique and match exactly file name in the dataset. Use in conjunction with <extra> option', type=int, default=None)
    parser.add_argument('-v', '--values', nargs='+', help='Indices of columns (starting from zero) to be joined. '
        'Use in conjunction with <extra> option', type=int, default=None)
    parser.add_argument('-r', '--rotate', help='CSV rolling', type=int, default=None)
    parser.add_argument('--remove_completed', help='Remove file after processing', action='store_true')
    parser.add_argument('--write_header', help='Write header to the output files', action='store_true')
    args = parser.parse_args()

    if args.output:
        output_filename = args.output
    else:
        output_filename = os.path.basename(os.path.normpath(args.directory))

    if args.extra or args.key or args.values:
        if not args.extra and args.key and args.values:
            raise ValueError('Extra, key and value options have to be used together or not at all')

    start = time.time()
    config = configure.read_config(args.config)
    classifier = ImageClassifier(config)
    writer = Writer(config, output_filename, write_header=args.write_header, rotate=args.rotate,
                    filename_with_extra_fields=args.extra, key_idx=args.key, val_idxs=args.values)

    failed_f = open('failed.txt', 'w', buffering=0)
    success_f = open('success.txt', 'w', buffering=0)

    for filename in glob2.iglob(os.path.join(args.directory, '**/*.jpg')):
        try:
            print('Processing: {}'.format(filename))
            with open(filename, 'rb') as f:
                result = classifier.get_prediction(f)
            writer.write(result)
            success_f.write(filename + '\n')
            if args.remove_completed:
                os.remove(filename)
        except Exception as ex:
            failed_f.write(filename + ';' + str(ex) + '\n')
            print('FAILED: ' + filename)


    print('Total time: {}'.format(time.time() - start))
    failed_f.close()
    success_f.close()