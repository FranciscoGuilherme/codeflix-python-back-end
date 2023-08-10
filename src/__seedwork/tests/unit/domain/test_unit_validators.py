import unittest
from unittest.mock import patch
from __seedwork.domain.validators import ValidatorRules
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
