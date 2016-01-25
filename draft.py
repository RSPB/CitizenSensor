import os
import re
import scipy.io
import numpy as np
import caffe
import gps
import configure

image_filepath = 'test/27302080E.jpg'
image_filepath2 = 'test/27742078S.jpg'

config = configure.read_config()

def normalise(array, cut_decimal_digits=None):
    normalised = (array - np.min(array)) / (np.max(array) - np.min(array))
    if cut_decimal_digits:
        normalised = np.round(normalised, cut_decimal_digits)
    return normalised

def get_mean_image(path):
    proto_obj = caffe.io.caffe_pb2.BlobProto()
    proto_file = open(path,'rb')
    proto_data = proto_file.read()
    proto_obj.ParseFromString(proto_data)
    means = np.asarray(proto_obj.data)
    return means.reshape(3,256,256).mean(1).mean(1)

if config['Algorithm']['use_gpu']:
    caffe.set_device(0)
    caffe.set_mode_gpu()
else:
    caffe.set_mode_cpu()
no_semantic_categories = config['Algorithm']['scene_attributes_no']
no_scene_attributes = config['Algorithm']['semantic_categories_no']

model_filepath = config['Model_filepaths']['network_definition']
pretrained_filepath = config['Model_filepaths']['caffe_model']
scene_attribute_model_filepath = config['Model_filepaths']['scene_attribute_model']
meanim_filepath = config['Model_filepaths']['meanimage_model']
labels_filename = config['Model_filepaths']['labels_model']

mean = get_mean_image(meanim_filepath)
scene_attribute_model = scipy.io.loadmat(scene_attribute_model_filepath)
W = scene_attribute_model['W_sceneAttribute']
attributes = scene_attribute_model['attributes']

net = caffe.Classifier(model_filepath, pretrained_filepath, mean=mean, channel_swap = (2, 1, 0),raw_scale = 255)
labels = np.loadtxt(labels_filename, str, delimiter='\t')

filename = os.path.splitext(os.path.basename(image_filepath))[0]
input_image = caffe.io.load_image(image_filepath)
prediction = net.predict([input_image])

# sort top k predictions from softmax output
top_semantic = prediction[0].argsort()[-1:-no_semantic_categories-1:-1]
top_semantic_labels = [unicode(re.match('([^\s]+)', label).group(1)) for label in labels[top_semantic]]
top_semantic_score = np.round(prediction[0][top_semantic], 3)
top_semantic_complete = zip(top_semantic_labels, top_semantic_score.tolist())

fc7 = net.blobs['fc7'].data
res = W.dot(fc7.T)

total_scene_score = normalise(res.sum(axis=1), 3)
top_scene_attr = total_scene_score.argsort()[-1:-no_scene_attributes-1:-1]
scene_attr_labels = attributes[top_scene_attr]
scene_attr = [scene_attr_labels[idx][0][0] for idx in range(10)]
scene_attr_score = total_scene_score[top_scene_attr]
scene_attr_complete = zip(scene_attr, scene_attr_score.tolist())

result = gps.get_gps_metadata(image_filepath)
result['semantic_categories'] = top_semantic_complete
result['scene_attributes'] = scene_attr_complete
print(result)