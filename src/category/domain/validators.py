from typing import Any
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator, StrictCharField, StrictBoolField


class CategoryRules(serializers.Serializer):
    name = serializers.StrictCharField(max_length=255)
    description = serializers.StrictCharField(required=False, allow_null=True)
    is_active = serializers.StrictBoolField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):

    def validate(self, data: Any):
        rules = CategoryRules(data=data)
        return super().validate(rules)


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return CategoryValidator()
