import os
import glob
import pandas as pd
import time
import configure
from image_classifier import ImageClassifier


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Batch classifier', prog='Citizen Sensor')
    parser.add_argument('-d', '--directory', help='Path to the directory with images', required=True)
    parser.add_argument('-o', '--output', help='Output filename', required=True)
    args = parser.parse_args()

    start = time.time()
    config = configure.read_config()
    classifier = ImageClassifier(config)

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    semantic_filename = os.path.join(output_dir, args.output + '.semantic')
    scene_filename = os.path.join(output_dir, args.output + '.scene')

    df_semantic = pd.DataFrame()
    df_scene = pd.DataFrame()

    for filename in glob.glob(os.path.join(args.directory, '*.jpg')):
        print('Processing: {}'.format(filename))
        with open(filename, 'rb') as f:
            result = classifier.get_prediction(f)
        df_semantic = df_semantic.append(result.semantic_scores, ignore_index=True)
        df_scene = df_scene.append(result.scene_scores, ignore_index=True)

    df_semantic.to_csv(semantic_filename + '_complete.csv', index=False)
    df_scene.to_csv(scene_filename + '_complete.csv', index=False)

    print('Total time: {}'.format(time.time() - start))