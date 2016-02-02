import os
import numpy as np
import scipy.io

class Writer(object):

    def __init__(self, config, output_filename, rotate=None):
        self.rotate = rotate
        self.files_processed = 0
        self.delimiter = ','
        self.format = '%s'
        output_dir = 'output'
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
        self.semantic_labels_filename = np.insert(semantic_labels, 0, 'Filename')

        scene_attribute_model_filepath = config['Model_filepaths']['scene_attribute_model']
        scene_attribute_model = scipy.io.loadmat(scene_attribute_model_filepath)
        scene_labels = np.asarray([attribute[0][0] for attribute in scene_attribute_model['attributes']])
        self.scene_labels_filename = np.insert(scene_labels, 0, 'Filename')
        self.formatting_precision = config['Algorithm']['formatting_precision']

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
            self.write_headers()


    def write(self, prediction):
        with open(self.output_filename_semantic, 'ab') as semantic_f:
            semantic_f.write(prediction.id + ',')
            semantic_f.write(','.join("%.2f" % number for number in prediction.semantic_scores))
            semantic_f.write('\n')
        with open(self.output_filename_scene, 'ab') as scene_f:
            scene_f.write(prediction.id + ',')
            scene_f.write(','.join("%.2f" % number for number in prediction.scene_scores))
            scene_f.write('\n')
        with open(self.output_filename_fc7, 'ab') as fc7_f:
            fc7_flat = prediction.fc7[(0,9),:].flatten()
            fc7_f.write(prediction.id + ',')
            fc7_f.write(','.join("%.4f" % number for number in fc7_flat))
            fc7_f.write('\n')
        self.files_processed += 1
        if self.rotate:
            self.rotate_output_filename()


if __name__ == '__main__':
    import configure
    from image_classifier import ImageClassifier

    config = configure.read_config()
    writer = Writer(config, 'test')
    classifier = ImageClassifier(config)
    writer.write_headers()
    with open('test/images/27302080E.jpg', 'rb') as testimage_f:
        p = classifier.get_prediction(testimage_f)
    writer.write(p)
