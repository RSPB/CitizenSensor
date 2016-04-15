import configure
import caffe
import numpy as np
import pandas as pd
import scipy.io

image_filepath = 'test/images/27302080E.jpg'

config = configure.read_config('output/config.ini')

class Prediction(object):

    def __init__(self, id, semantic_scores, scene_scores):
        self.id = id
        self.semantic_scores = semantic_scores
        self.scene_scores = scene_scores

def get_mean_image(path):
    proto_obj = caffe.io.caffe_pb2.BlobProto()
    proto_file = open(path,'rb')
    proto_data = proto_file.read()
    proto_obj.ParseFromString(proto_data)
    means = np.asarray(proto_obj.data)
    return means.reshape(3,256,256).mean(1).mean(1)

def format_array_as_list(array, precision):
    return [round(number, precision) for number in array.tolist()]

if config['Algorithm']['use_gpu']:
    caffe.set_device(0)
    caffe.set_mode_gpu()
else:
    caffe.set_mode_cpu()

no_semantic_categories = config['Algorithm']['scene_attributes_no']
no_scene_attributes = config['Algorithm']['semantic_categories_no']
formatting_precision = config['Algorithm']['formatting_precision']

model_filepath = config['Model_filepaths']['network_definition']
pretrained_filepath = config['Model_filepaths']['caffe_model']
scene_attribute_model_filepath = config['Model_filepaths']['scene_attribute_model']
meanim_filepath = config['Model_filepaths']['meanimage_model']
labels_filename = config['Model_filepaths']['labels_model']

# mean = get_mean_image(meanim_filepath)
mean = np.array([105.908874512, 114.063842773, 116.282836914])
scene_attribute_model = scipy.io.loadmat(scene_attribute_model_filepath)
W = scene_attribute_model['W_sceneAttribute']
attributes = scene_attribute_model['attributes']
scene_labels = np.asarray([attribute[0][0] for attribute in attributes ])

net = caffe.Classifier(model_filepath, pretrained_filepath, mean=mean, channel_swap = (2, 1, 0),raw_scale = 255)
semantic_labels = np.loadtxt(labels_filename, str, delimiter=' ')[:,0]

input_image = caffe.io.load_image(image_filepath)
prediction = net.predict([input_image])

# sort top k predictions from softmax output
top_semantic = prediction[0].argsort()[-1:-no_semantic_categories-1:-1]
top_semantic_labels = semantic_labels[top_semantic]
top_semantic_score = prediction[0][top_semantic]
top_semantic_score_rounded = format_array_as_list(top_semantic_score, formatting_precision)
top_semantic_complete = zip(top_semantic_labels, top_semantic_score_rounded)

fc7 = net.blobs['fc7'].data
res = W.dot(fc7.T)

total_scene_score = res.sum(axis=1)

scene_attributes = W.dot(fc7.T)
total_scene_scores = scene_attributes.sum(axis=1)
semantic_scores = pd.Series(prediction[0], semantic_labels, dtype=pd.np.float16)
scene_scores = pd.Series(total_scene_scores,  scene_labels, dtype=pd.np.float16)
prediction = Prediction(id=image_filepath, semantic_scores=semantic_scores, scene_scores=scene_scores)