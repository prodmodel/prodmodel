import transform_record
import unittest


class TestTransformRecord(unittest.TestCase):

    def test_rich(self):
        self.assertEqual(transform_record._rich({'marital': 'single', 'balance': 600}), True)
