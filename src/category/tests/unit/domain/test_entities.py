import unittest
from datetime import datetime
from unittest.mock import patch
from dataclasses import is_dataclass, FrozenInstanceError
from category.domain.entities import Category


class TestCategory(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Category))

    def test_constructor(self) -> None:
        with patch.object(Category, "validate") as mock_validate_method:
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
        mock_validate_method.assert_called_once()

    def test_constructor_default_data(self) -> None:
        with patch.object(Category, "validate"):
            category = Category(name="Movie")
            self.assertEqual(category.name, "Movie")
            self.assertIsNone(category.description)
            self.assertTrue(category.is_active)
            self.assertIsInstance(category.created_at, datetime)

    def test_if_created_at_is_generated_in_constructor(self) -> None:
        with patch.object(Category, "validate"):
            category1 = Category(name="Movie 1")
            category2 = Category(name="Movie 2")
            self.assertNotEqual(
                category1.created_at.timestamp(),
                category2.created_at.timestamp()
            )

    def test_is_immutable(self) -> None:
        with patch.object(Category, "validate"):
            with self.assertRaises(FrozenInstanceError):
                category = Category(name="Documentary")
                category.name = "fake id"

    def test_update_name_and_description_properties(self) -> None:
        with patch.object(Category, "validate"):
            category = Category(name="Movie")
            category.update("Documentary", "This is a description")
            self.assertEqual(category.name, "Documentary")
            self.assertEqual(category.description, "This is a description")

    def test_update_name_property_only(self) -> None:
        with patch.object(Category, "validate"):
            with patch.object(
                Category,
                "update",
                autospec=True,
                side_effect=Category.update
            ) as category_mock:
                category = Category(name="Movie")
                category.update("Documentary")
                self.assertEqual(category.name, "Documentary")
                self.assertIsNone(category.description)
                category_mock.assert_called_once()

    def test_should_activate_a_category(self) -> None:
        with patch.object(Category, "validate"):
            with patch.object(
                Category,
                "activate",
                autospec=True,
                side_effect=Category.activate
            ) as category_mock:
                category = Category(name="Movie", is_active=False)
                category.activate()
                self.assertTrue(category.is_active)
                category_mock.assert_called_once()

    def test_should_deactivate_a_category(self) -> None:
        with patch.object(Category, "validate"):
            with patch.object(
                Category,
                "deactivate",
                autospec=True,
                side_effect=Category.deactivate
            ) as category_mock:
                category = Category(name="Movie")
                category.deactivate()
                self.assertFalse(category.is_active)
                category_mock.assert_called_once()
