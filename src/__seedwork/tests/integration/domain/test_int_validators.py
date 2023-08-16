import unittest
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator


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
