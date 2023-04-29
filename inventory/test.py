from django.test import TestCase

# Create your tests here.
import unittest
import accounts



class TestSum(unittest.TestCase):
    def test_list_int(self):
        sample = views.index()
        self.assertIsNotNone(sample)
        

if __name__ == '__main__':
    unittest.main()