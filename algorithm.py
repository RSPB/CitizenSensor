#!/usr/bin/env python

import os
import re
import scipy.io
import numpy as np
import caffe
from gps import GPSLocator

class Classifier(object):

    def __init__(self):
        caffe.set_device(0)
        caffe.set_mode_gpu()
        caffe_root = '/home/tracek/Libraries/caffe/'
        self.no_semantic_categories = 5
        self.no_scene_attributes = 10
        self.locator = GPSLocator()

        model_filepath = caffe_root + 'models/places205CNN/places205CNN_deploy_upgraded.prototxt'
        pretrained_filepath = caffe_root + 'models/places205CNN/places205CNN_iter_300000_upgraded.caffemodel'
        scene_attribute_model_filepath = caffe_root + 'models/places205CNN/sceneAttributeModel205.mat'
        meanim_filepath = caffe_root + 'models/places205CNN/places205CNN_mean.binaryproto'
        labels_filename = caffe_root + 'models/places205CNN/categoryIndex_places205.csv'

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


if __name__ == '__main__':
    classifier = Classifier()
    image_filepath = '/home/tracek/Notebooks/data/27302080E.jpg'
    result = classifier.identify_image(image_filepath)
    print result

