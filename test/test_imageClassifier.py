import configure
from image_classifier import ImageClassifier
from unittest import TestCase

classification_27302080E = {
 'altitude': 774,
 'date': '2012-05-18',
 'datum': 'WGS-84',
 'position': (40.031789120069355, 8.757675880026039),
 'scene_attributes': [(u'natural light', 1.0),
  (u'trees', 0.8274839766613612),
  (u'vegetation', 0.7802953337324795),
  (u'natural', 0.754969957563941),
  (u'open area', 0.734384217685197),
  (u'foliage', 0.7247446972790146),
  (u'nohorizon', 0.7108939222006811),
  (u'shrubbery', 0.6926026467029156),
  (u'sunny', 0.6419471517328291),
  (u'vertical components', 0.6285095715278544)],
 'semantic_categories': [('swamp', 0.6760071516036987),
  ('forest_path', 0.08620761334896088),
  ('marsh', 0.04093477874994278),
  ('orchard', 0.02828938327729702),
  ('boardwalk', 0.02402796410024166)]}

class TestImageClassifier(TestCase):

    def test_identify_image(self):
        config = configure.read_config()
        classifier = ImageClassifier(config)
        res = classifier.identify_image('test/27302080E.jpg')
        self.maxDiff = None # print full diff on mismatch
        self.assertDictEqual(res, classification_27302080E)