import unittest
from category.domain.validators import CategoryValidatorFactory, CategoryValidator


class TestCategoryValidatorIntegration(unittest.TestCase):

    validator: CategoryValidator

    def setUp(self) -> None:
        self.validator = CategoryValidatorFactory.create()

    def test_if_is_invalid(self) -> None:
        invalid_data: list = [
            {
                "data": {"name": None},
                "error": ["This field may not be null."]
            },
            {
                "data": {"name": ""},
                "error": ["This field may not be blank."]
            },
            {
                "data": {"name": 5},
                "error": ["Not a valid string."]
            },
            {
                "data": {"name": "t" * 256},
                "error": ["Ensure this field has no more than 255 characters."]
            }
        ]
        for i in invalid_data:
            self.assertFalse(self.validator.validate(i["data"]))
            self.assertListEqual(self.validator.errors["name"], i["error"])

    def test_if_is_valid(self) -> None:
        self.assertTrue(self.validator.validate({"name": "name"}))
