import unittest
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator, StrictCharField, StrictBoolField


class StubSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.IntegerField()


class TestDRFValidatorIntegration(unittest.TestCase):

    def test_validation_with_errors(self) -> None:
        validator = DRFValidator()
        serializer = StubSerializer(data={})
        is_valid: bool = validator.validate(serializer)
        self.assertFalse(is_valid)
        self.assertEqual(validator.errors, {
            "name": ["This field is required."],
            "price": ["This field is required."]
        })

    def test_validation_without_errors(self) -> None:
        validator = DRFValidator()
        serializer = StubSerializer(data={"name": "value", "price": 5})
        is_valid: bool = validator.validate(serializer)
        self.assertTrue(is_valid)
        self.assertEqual(
            validator.validated_data,
            {
                "name": "value",
                "price": 5
            })


class TestStrictCharFieldUnit(unittest.TestCase):

    def test_if_is_invalid_when_not_str_values(self) -> None:
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField()

        invalid_data: list = [
            {"name": 5},
            {"name": True}
        ]

        for i in invalid_data:
            serializer = StubStrictCharFieldSerializer(data=i)
            serializer.is_valid()
            self.assertEqual(serializer.errors, {
                "name": [serializers.ErrorDetail(string="Not a valid string.", code="invalid")]
            })

    def test_none_value_is_valid(self) -> None:
        class StubStrictCharFieldSerializer(serializers.Serializer):
            name = StrictCharField(required=False, allow_null=True)

        serializer = StubStrictCharFieldSerializer(data={"name": None})
        self.assertTrue(serializer.is_valid())

    def test_if_is_invalid_when_not_boolean_values(self) -> None:
        class StubStrictBooleanFieldSerializer(serializers.Serializer):
            name = StrictBoolField()

        invalid_data: list = [
            {"name": 0},
            {"name": 1},
            {"name": ""},
            {"name": "True"},
            {"name": "False"}
        ]

        for i in invalid_data:
            serializer = StubStrictBooleanFieldSerializer(data=i)
            serializer.is_valid()
            self.assertEqual(serializer.errors, {
                "name": [serializers.ErrorDetail(string="Must be a valid boolean.", code="invalid")]
            })
