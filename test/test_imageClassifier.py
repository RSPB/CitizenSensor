import configure
from image_classifier import ImageClassifier
from unittest import TestCase
from numpy import testing

classification_27302080E = {
 'altitude': 774,
 'date': '2012-05-18',
 'datum': 'WGS-84',
 'position': (40.031789120069355, 8.757675880026039),
 'scene_attributes':
     [(u'natural light', 1.0),
      (u'trees', 0.827),
      (u'vegetation', 0.78),
      (u'natural', 0.755),
      (u'open area', 0.734),
      (u'foliage', 0.725),
      (u'nohorizon', 0.711),
      (u'shrubbery', 0.693),
      (u'sunny', 0.642),
      (u'vertical components', 0.629)],
 'semantic_categories':
     [('swamp', 0.676),
      ('forest_path', 0.086),
      ('marsh', 0.041),
      ('orchard', 0.028),
      ('boardwalk', 0.024)]}

class TestImageClassifier(TestCase):

    def test_identify_image(self):
        config = configure.read_config()
        config['Algorithm']['semantic_categories_no'] = 10
        config['Algorithm']['scene_attributes_no'] = 5
        config['GPS']['reverse_location'] = False
        classifier = ImageClassifier(config)
        res = classifier.identify_image('test/27302080E.jpg')
        self.maxDiff = None # print full diff on mismatch
        self.assertDictEqual(res, classification_27302080E)