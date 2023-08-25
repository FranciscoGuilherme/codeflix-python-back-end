from typing import Dict
from rest_framework import serializers
from __seedwork.domain.validators import DRFValidator, StrictCharField, StrictBoolField


class CategoryRules(serializers.Serializer):
    name = StrictCharField(max_length=255)
    description = StrictCharField(required=False, allow_null=True)
    is_active = StrictBoolField(required=False)
    created_at = serializers.DateTimeField(required=False)


class CategoryValidator(DRFValidator):

    def validate(self, data: Dict):
        rules = CategoryRules(data=data if data is not None else {})
        return super().validate(rules)


class CategoryValidatorFactory:

    @staticmethod
    def create():
        return CategoryValidator()
