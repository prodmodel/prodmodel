import transform_record
import feature_definitions
import unittest


class TestTransformRecord(unittest.TestCase):

    def test_transform_record(self):
        self.assertEqual(transform_record.transform_record(
            {'marital': 'single', 'balance': 600, 'education': 'primary'}, {'primary': 100}),
            {'marital': 'single', 'balance': 600, 'education': 'primary', 'education_score': 100, 'rich': True})


    def test_rich(self):
        self.assertEqual(feature_definitions.rich({'marital': 'single', 'balance': 600}), True)
