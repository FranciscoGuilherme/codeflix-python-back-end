import unittest
from category.domain.entities import Category
from __seedwork.domain.exceptions import ValidationException


class TestCategoryIntegration(unittest.TestCase):

    def test_should_throw_an_exception_when_pass_invalid_name_data_on_create(self) -> None:
        invalid_data = [
            {"value": "", "message": "The name is required"},
            {"value": None, "message": "The name is required"},
            {"value": 1000, "message": "The name must be a string"},
            {"value": "t" * 256, "message": "The name must be less than 255 characters"}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                Category(name=i["value"])
            self.assertEqual(i["message"], assert_error.exception.args[0])

    def test_should_throw_an_exception_when_pass_invalid_description_data_on_create(self) -> None:
        invalid_data = [
            {"value": 5},
            {"value": 5.0},
            {"value": []},
            {"value": {}},
            {"value": True},
            {"value": False},
            {"value": 10000}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                Category(name="Documentary", description=i["value"])
            self.assertEqual("The description must be a string", assert_error.exception.args[0])

    def test_should_throw_an_exception_when_pass_invalid_is_active_data_on_create(self) -> None:
        invalid_data = [
            {"value": 5},
            {"value": 5.0},
            {"value": []},
            {"value": {}},
            {"value": "True"},
            {"value": "False"},
            {"value": 1000000}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                Category(name="Documentary", is_active=i["value"])
            self.assertEqual("The is_active must be a boolean", assert_error.exception.args[0])

    def test_valid_cases_on_create(self) -> None:
        try:
            Category(name="Documentary")
            Category(name="Documentary", description=None)
            Category(name="Documentary", description="")
            Category(name="Documentary", description="some description")
            Category(name="Documentary", is_active=True)
            Category(name="Documentary", is_active=False)
            Category(
                name="Documentary",
                description="some description",
                is_active=False
            )
        except ValidationException as exception:
            self.fail(f"Some prop is not valid. Error: {exception.args[0]}")

    def test_should_throw_an_exception_when_pass_invalid_name_data_on_update(self) -> None:
        invalid_data = [
            {"value": "", "message": "The name is required"},
            {"value": None, "message": "The name is required"},
            {"value": 1000, "message": "The name must be a string"},
            {"value": "t" * 256, "message": "The name must be less than 255 characters"}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                Category(name="Documentary").update(name=i["value"])
            self.assertEqual(i["message"], assert_error.exception.args[0])

    def test_should_throw_an_exception_when_pass_invalid_description_data_on_update(self) -> None:
        invalid_data = [
            {"value": 5},
            {"value": 5.0},
            {"value": []},
            {"value": {}},
            {"value": True},
            {"value": False},
            {"value": 10000}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                Category(name="Documentary", description=None).update(name="Movie", description=i["value"])
            self.assertEqual("The description must be a string", assert_error.exception.args[0])

    def test_valid_cases_on_update(self) -> None:
        category = Category(name="Documentary")
        try:
            category.update(name="Movie")
            category.update(name="Movie", description=None)
            category.update(name="Movie", description="")
            category.update(name="Movie", description="some description")
        except ValidationException as exception:
            self.fail(f"Some prop is not valid. Error: {exception.args[0]}")
