import unittest
from dataclasses import fields
from unittest.mock import patch
from __seedwork.domain.validators import ValidatorRules, ValidatorFieldsInterface
from __seedwork.domain.exceptions import ValidationException


class TestValidatorRules(unittest.TestCase):

    def test_values_methods(self) -> None:
        validator = ValidatorRules.values("value", "prop")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "value")
        self.assertEqual(validator.prop, "prop")

    def test_should_throw_an_error_when_try_to_validate_required(self) -> None:
        invalid_data = [
            {"value": ""},
            {"value": None}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="required",
            autospec=True,
            side_effect=ValidatorRules.required
        ) as validator_mock:
            for i in invalid_data:
                with self.assertRaises(ValidationException, msg=f"Value {i['value']} dit not raise") as assert_error:
                    ValidatorRules.values(i["value"], "prop").required()
                self.assertEqual("The prop is required", assert_error.exception.args[0])
            self.assertEqual(validator_mock.call_count, len(invalid_data))

    def test_required_rule_valid_data(self) -> None:
        valid_data = [
            {"value": 0},
            {"value": 5},
            {"value": 5.1},
            {"value": True},
            {"value": []}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="required",
            autospec=True,
            side_effect=ValidatorRules.required
        ) as validator_mock:
            for i in valid_data:
                ValidatorRules.values(i["value"], "prop").required()
            self.assertEqual(validator_mock.call_count, len(valid_data))

    def test_should_throw_an_error_when_try_to_validate_string(self) -> None:
        invalid_data = [
            {"value": 0},
            {"value": 5},
            {"value": 5.1},
            {"value": True},
            {"value": []},
            {"value": {}}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="string",
            autospec=True,
            side_effect=ValidatorRules.string
        ) as validator_mock:
            for i in invalid_data:
                with self.assertRaises(ValidationException, msg=f"Value {i['value']} dit not raise") as assert_error:
                    ValidatorRules.values(i["value"], "prop").string()
                self.assertEqual("The prop must be a string", assert_error.exception.args[0])
            self.assertEqual(validator_mock.call_count, len(invalid_data))

    def test_string_rule_valid_data(self) -> None:
        valid_data = [
            {"value": ""},
            {"value": None},
            {"value": "None"},
            {"value": "True"}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="string",
            autospec=True,
            side_effect=ValidatorRules.string
        ) as validator_mock:
            for i in valid_data:
                ValidatorRules.values(i["value"], "prop").string()
            self.assertEqual(validator_mock.call_count, len(valid_data))

    def test_should_throw_an_error_when_try_to_validate_max_length(self) -> None:
        invalid_data = [
            {"value": "t" * 5}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="max_length",
            autospec=True,
            side_effect=ValidatorRules.max_length
        ) as validator_mock:
            for i in invalid_data:
                with self.assertRaises(ValidationException, msg=f"Value {i['value']} dit not raise") as assert_error:
                    ValidatorRules.values(i["value"], "prop").max_length(4)
                self.assertEqual("The prop must be less than 4 characters", assert_error.exception.args[0])
            self.assertEqual(validator_mock.call_count, len(invalid_data))

    def test_max_length_rule_valid_data(self) -> None:
        valid_data = [
            {"value": "t"},
            {"value": None},
            {"value": "None"},
            {"value": "True"}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="max_length",
            autospec=True,
            side_effect=ValidatorRules.max_length
        ) as validator_mock:
            for i in valid_data:
                ValidatorRules.values(i["value"], "prop").max_length(5)
            self.assertEqual(validator_mock.call_count, len(valid_data))

    def test_should_throw_an_error_when_try_to_validate_boolean(self) -> None:
        invalid_data = [
            {"value": 0},
            {"value": 5},
            {"value": 5.1},
            {"value": []},
            {"value": {}},
            {"value": "True"},
            {"value": "False"}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="boolean",
            autospec=True,
            side_effect=ValidatorRules.boolean
        ) as validator_mock:
            for i in invalid_data:
                with self.assertRaises(ValidationException, msg=f"Value {i['value']} dit not raise") as assert_error:
                    ValidatorRules.values(i["value"], "prop").boolean()
                self.assertEqual("The prop must be a boolean", assert_error.exception.args[0])
            self.assertEqual(validator_mock.call_count, len(invalid_data))

    def test_boolean_rule_valid_data(self) -> None:
        valid_data = [
            {"value": None},
            {"value": True},
            {"value": False}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="boolean",
            autospec=True,
            side_effect=ValidatorRules.boolean
        ) as validator_mock:
            for i in valid_data:
                ValidatorRules.values(i["value"], "prop").boolean()
            self.assertEqual(validator_mock.call_count, len(valid_data))

    def test_should_throw_a_validation_exception_when_combine_two_or_more_rules(self) -> None:
        length: int = 2
        invalid_data = [
            {"value": None, "message": "The prop is required"},
            {"value": 1000, "message": "The prop must be a string"},
            {"value": "1000", "message": f"The prop must be less than {length} characters"}
        ]
        for i in invalid_data:
            with self.assertRaises(ValidationException) as assert_error:
                ValidatorRules.values(i["value"], "prop").required().string().max_length(length)
            self.assertEqual(i["message"], assert_error.exception.args[0])

    def test_valid_rules_combination(self) -> None:
        valid_data = [
            {"value": "value 1"},
            {"value": "value two"},
            {"value": "something else"}
        ]
        with patch.object(
            target=ValidatorRules,
            attribute="string",
            autospec=True,
            side_effect=ValidatorRules.string
        ) as validator_mock:
            for i in valid_data:
                ValidatorRules.values(i["value"], "prop").required().string().max_length(50)
        self.assertEqual(validator_mock.call_count, len(valid_data))


class TestValidatorFieldsInterface(unittest.TestCase):

    def test_should_throw_an_exception_when_try_create_an_instance_method_not_implemented(self) -> None:
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()
        self.assertEqual(
            "Can't instantiate abstract class ValidatorFieldsInterface with abstract method validate",
            assert_error.exception.args[0]
        )

    def test_interface_fields(self) -> None:
        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        validated_data_field = fields_class[1]
        self.assertEqual(errors_field.name, "errors")
        self.assertIsNone(errors_field.default)
        self.assertEqual(validated_data_field.name, "validated_data")
        self.assertIsNone(validated_data_field.default)
