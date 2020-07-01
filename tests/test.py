"""
Unit testing of the automatic batch processing application
"""
import unittest
 
class AppTests(unittest.TestCase):
    def test_app(self):
        """Simple Tests"""
        self.assertEqual(1, 1)
        self.assertNotEqual(2, 5)
 
def suite():
    _suite = unittest.TestSuite()
    _suite.addTest(AppTests('test_app'))
    return _suite
