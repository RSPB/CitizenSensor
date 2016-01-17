#!/usr/bin/env python

import os
import re
import scipy.io
import numpy as np
import caffe
from gps import GPSLocator

class ImageClassifier(object):
    """
    Image classifier based on convolutional neural networks.

    The image classifier uses model trained on MIT Places Database and is based on:
    "Learning Deep Features for Scene Recognition using Places Database" B. Zhou et al.
    """

    def __init__(self, config):
        """
        :param config: configuration file ini-style
        """
        if config['Algorithm']['use_gpu']:
            caffe.set_device(0)
            caffe.set_mode_gpu()
        else:
            caffe.set_mode_cpu()
        self.no_semantic_categories = config['Algorithm']['scene_attributes_no']
        self.no_scene_attributes = config['Algorithm']['semantic_categories_no']
        self.locator = GPSLocator()

        model_filepath = config['Model_filepaths']['network_definition']
        pretrained_filepath = config['Model_filepaths']['caffe_model']
        scene_attribute_model_filepath = config['Model_filepaths']['scene_attribute_model']
        meanim_filepath = config['Model_filepaths']['meanimage_model']
        labels_filename = config['Model_filepaths']['labels_model']

        mean = self.get_mean_image(meanim_filepath)
        scene_attribute_model = scipy.io.loadmat(scene_attribute_model_filepath)
        self.W = scene_attribute_model['W_sceneAttribute']
        self.attributes = scene_attribute_model['attributes']

        self.net = caffe.Classifier(model_filepath, pretrained_filepath, mean=mean, channel_swap = (2, 1, 0),raw_scale = 255)
        self.labels = np.loadtxt(labels_filename, str, delimiter='\t')

    def get_mean_image(self, path):
        proto_obj = caffe.io.caffe_pb2.BlobProto()
        proto_file = open(path,'rb')
        proto_data = proto_file.read()
        proto_obj.ParseFromString(proto_data)
        means = np.asarray(proto_obj.data)
        return means.reshape(3,256,256).mean(1).mean(1)

    def normalize(self, array):
        return (array - min(array)) / (max(array) - min(array))

    def identify_image(self, image_filepath):
        filename = os.path.splitext(os.path.basename(image_filepath))[0]
        input_image = caffe.io.load_image(image_filepath)
        prediction = self.net.predict([input_image])

        # sort top k predictions from softmax output
        top_semantic = prediction[0].argsort()[-1:-self.no_semantic_categories-1:-1]
        top_semantic_labels = [re.match('([^\s]+)', label).group(1) for label in self.labels[top_semantic]]
        top_semantic_score = prediction[0][top_semantic]
        top_semantic_complete = zip(top_semantic_labels, top_semantic_score.tolist())

        fc7 = self.net.blobs['fc7'].data
        res = self.W.dot(fc7.T)

        total_scene_score = self.normalize(res.sum(axis=1))
        top_scene_attr = total_scene_score.argsort()[-1:-self.no_scene_attributes-1:-1]
        scene_attr_labels = self.attributes[top_scene_attr]
        scene_attr = [scene_attr_labels[idx][0][0] for idx in range(10)]
        scene_attr_score = total_scene_score[top_scene_attr]
        scene_attr_complete = zip(scene_attr, scene_attr_score.tolist())

        result = self.locator.get_gps_metadata(image_filepath)
        result['semantic_categories'] = top_semantic_complete
        result['scene_attributes'] = scene_attr_complete

        return result


def _check_file_exist(path):
    if not os.path.isfile(path):
        raise argparse.ArgumentTypeError('{0} does not exist'.format(path))
    return path

if __name__ == '__main__':
    import argparse
    from configobj import ConfigObj
    from validate import Validator

    parser = argparse.ArgumentParser(description='Image classifier.', prog='Citizen Sensor')
    parser.add_argument('-i', '--image', help='Path to an image', type=_check_file_exist, required=True)
    parser.add_argument('-c', '--config', help='Path to ini config file',
                        default=os.path.join(os.environ['HOME'], '.citizen-sensor', 'config.ini'), type=_check_file_exist)
    args = parser.parse_args()

    config = ConfigObj(args.config, )
    classifier = ImageClassifier(config)
    result = classifier.identify_image(args.image)
    print result

