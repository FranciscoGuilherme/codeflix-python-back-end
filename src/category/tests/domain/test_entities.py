import unittest
from datetime import datetime
from dataclasses import is_dataclass
from category.domain.entities import Category

class TestCategory(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self) -> None:
        category = Category(
            name="Movie",
            description="some description",
            is_active=False,
            created_at=datetime.now()
        )
        self.assertEqual(category.name, "Movie")
        self.assertEqual(category.description, "some description")
        self.assertFalse(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

    def test_constructor_default_data(self) -> None:
        category = Category(name="Movie")
        self.assertEqual(category.name, "Movie")
        self.assertEqual(category.description, None)
        self.assertTrue(category.is_active)
        self.assertIsInstance(category.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self) -> None:
        category1 = Category(name="Movie 1")
        category2 = Category(name="Movie 2")
        self.assertNotEqual(
            category1.created_at.timestamp(),
            category2.created_at.timestamp()
        )
