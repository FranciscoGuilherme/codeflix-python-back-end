import unittest
from unittest.mock import patch, MagicMock
from category.domain.validators import DRFValidator, CategoryValidatorFactory


class TestCategoryValidatorUnit(unittest.TestCase):

    @patch.object(DRFValidator, "validate", return_value=True)
    def test_if_is_valid(self, mock_is_valid: MagicMock) -> None:
        self.assertTrue(CategoryValidatorFactory().create().validate({"name": "name"}))
        mock_is_valid.assert_called()
