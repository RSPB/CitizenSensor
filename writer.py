import os
import csv
import numpy as np
import scipy.io
from operator import itemgetter

def get_mapping(path, key_idx, val_idxs):
    d = {}
    with open(path, mode='r') as f:
        reader = csv.reader(f)
        header = reader.next()
        header = itemgetter(*val_idxs)(header)
        for row in reader:
            key = os.path.basename(row[key_idx])
            val = itemgetter(*val_idxs)(row)
            d[key] = val
    return d


class Writer(object):

    def __init__(self, config, output_filename, write_header=True, rotate=None, filename_with_extra_fields=None, key_idx=None, val_idxs=None):
        self.write_header = write_header
        self.rotate = rotate
        self.files_processed = 0
        self.delimiter = ','
        self.format = '%s'
        output_dir = 'output'

        if filename_with_extra_fields:
            self.val_idxs = val_idxs
            self.val_to_join = get_mapping(filename_with_extra_fields, key_idx, val_idxs)
        else:
            self.val_to_join = None

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        if rotate:
            self.rotate_idx = 1
            self.output_filename_semantic_template = os.path.join(output_dir, output_filename + '_semantic_{0:0>5}.csv')
            self.output_filename_scene_template = os.path.join(output_dir, output_filename + '_scene_{0:0>5}.csv')
            self.output_filename_fc7_template = os.path.join(output_dir, output_filename + '_fc7_{0:0>5}.csv')
            self.set_filename_idx()
        else:
            self.output_filename_semantic = os.path.join(output_dir, output_filename + '_semantic.csv')
            self.output_filename_scene = os.path.join(output_dir, output_filename + '_scene.csv')
            self.output_filename_fc7 = os.path.join(output_dir, output_filename + '_fc7.csv')

        semantic_labels_filename = config['Model_filepaths']['labels_model']
        semantic_labels = np.loadtxt(semantic_labels_filename, str, delimiter=' ')[:, 0]
        # self.semantic_labels_filename = np.insert(semantic_labels, 0,
        #                                           ['Filename', 'X', 'Y', 'gid', 'LC_level1', 'LC_level1_text',
        #                                            'LC_level1_num', 'LC_level2', 'LC_level2_text', 'LC_level2_num'])
        self.semantic_labels_filename = np.insert(semantic_labels, 0, 'Filename')

        scene_attribute_model_filepath = config['Model_filepaths']['scene_attribute_model']
        scene_attribute_model = scipy.io.loadmat(scene_attribute_model_filepath)
        scene_labels = np.asarray([attribute[0][0] for attribute in scene_attribute_model['attributes']])
        self.scene_labels_filename = np.insert(scene_labels, 0, 'Filename')
        self.formatting_precision = config['Algorithm']['formatting_precision']

        if self.write_header:
            self.write_headers()

    def write_headers(self):
        np.savetxt(self.output_filename_semantic, self.semantic_labels_filename.reshape((1,-1)), delimiter=self.delimiter, fmt=self.format)
        np.savetxt(self.output_filename_scene, self.scene_labels_filename.reshape((1,-1)), delimiter=self.delimiter, fmt=self.format)

    def set_filename_idx(self):
        self.output_filename_semantic = self.output_filename_semantic_template.format(self.rotate_idx)
        self.output_filename_scene = self.output_filename_scene_template.format(self.rotate_idx)
        self.output_filename_fc7 = self.output_filename_fc7_template.format(self.rotate_idx)

    def rotate_output_filename(self):
        if self.files_processed % self.rotate == 0:
            self.rotate_idx += 1
            self.set_filename_idx()
            if self.write_header:
                self.write_headers()

    def write_single(self, filename, prediction_id, array, precision):
        with open(filename, 'ab') as f:
            f.write(prediction_id + ',')
            if self.val_to_join:
                # prediction_id = os.path.splitext(prediction_id)[0]
                # if any(x == prediction_id[-1] for x in ['P', 'W', 'E', 'N', 'S']):
                #     prediction_id = prediction_id[:-1]
                vals = self.val_to_join.get(prediction_id)
                if vals:
                    f.write(','.join(val for val in vals))
                    f.write(',')
                else:
#                    raise KeyError('id {} not found'.format(prediction_id))
                    [f.write(',') for i in self.val_idxs]
            f.write(','.join(precision % number for number in array))
            f.write('\n')


    def write(self, prediction):
        self.write_single(self.output_filename_semantic, prediction.id, prediction.semantic_scores, "%.2f")
        self.write_single(self.output_filename_scene, prediction.id, prediction.scene_scores, "%.2f")
        self.write_single(self.output_filename_fc7, prediction.id, prediction.fc7[(0,9),:].flatten(), "%.4f" )
        # self.write_single(self.output_filename_fc7, prediction.id, prediction.fc7[0], "%.4f" )

        self.files_processed += 1
        if self.rotate:
            self.rotate_output_filename()


if __name__ == '__main__':
    import configure
    from image_classifier import ImageClassifier

    config = configure.read_config()
    writer = Writer(config, 'test', filename_with_extra_fields='data/evaluation_3k_set.csv', key_idx=1, val_idxs=[0,3,4])
    classifier = ImageClassifier(config)
    writer.write_headers()
    with open('test/images/3221567431_a58ffbd628.jpg', 'rb') as testimage_f:
        p = classifier.get_prediction(testimage_f)
    writer.write(p)
