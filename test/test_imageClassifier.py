import configure
from image_classifier import ImageClassifier
from unittest import TestCase
from nose.plugins.attrib import attr

classification_27302080E = {
 'ApertureValue': 3.93,
 'LightSource': 'Unknown',
 'Orientation': 'Horizontal (normal)',
 'SceneCaptureType': 'Standard',
 'ShutterSpeedValue': 0.004,
 'SubjectDistance': 'Unknown',
 'SubjectDistanceRange': '0',
 'altitude': 774,
 'date': '2012-05-18',
 'datum': 'WGS-84',
 'filename': 'test/images/27302080E.jpg',
 'position': (40.031789120069355, -8.757675880026039),
 'scene_attributes':
     [(u'natural light', 154.569),
      (u'trees', 84.931),
      (u'vegetation', 65.883),
      (u'natural', 55.66),
      (u'open area', 47.35),
      (u'foliage', 43.459),
      (u'nohorizon', 37.868),
      (u'shrubbery', 30.485),
      (u'sunny', 10.037),
      (u'vertical components', 4.613)],
 'semantic_categories':
     [('swamp', 0.676),
      ('forest_path', 0.086),
      ('marsh', 0.041),
      ('orchard', 0.028),
      ('boardwalk', 0.024)]}

class TestImageClassifier(TestCase):

    @attr('slow')
    def test_identify_image(self):
        config = configure.read_config()
        config['Algorithm']['semantic_categories_no'] = 10
        config['Algorithm']['scene_attributes_no'] = 5
        config['Algorithm']['formatting_precision'] = 3
        config['GPS']['reverse_location'] = False
        classifier = ImageClassifier(config)
        res = classifier.identify_image('test/images/27302080E.jpg')
        self.maxDiff = None # print full diff on mismatch
        self.assertDictEqual(res, classification_27302080E)