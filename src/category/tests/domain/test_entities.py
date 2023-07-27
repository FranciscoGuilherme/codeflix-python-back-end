import unittest
from datetime import datetime
from category.domain.entities import Category

class TestCategory(unittest.TestCase):
    def test_constructor(self):
        category = Category("Movie", "some description", True, datetime.now())
        self.assertEqual(category.name, "Movie1")
