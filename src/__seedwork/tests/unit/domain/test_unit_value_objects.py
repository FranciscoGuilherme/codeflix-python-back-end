import uuid
import unittest
from abc import ABC
from unittest.mock import patch
from dataclasses import dataclass, is_dataclass, FrozenInstanceError
from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import ValueObject, UniqueEntityId


@dataclass(frozen=True)
class StubOneProp(ValueObject):
    prop: str


@dataclass(frozen=True)
class StubTwoProps(ValueObject):
    prop1: str
    prop2: str


class TestValueObjectUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self) -> None:
        self.assertTrue(is_dataclass(ValueObject))

    def test_if_is_instance_of_abstract_class(self) -> None:
        self.assertIsInstance(ValueObject(), ABC)

    def test_init_prop(self) -> None:
        value_object_one_prop = StubOneProp(prop="message")
        self.assertEqual(value_object_one_prop.prop, "message")

        value_object_two_props = StubTwoProps(
            prop1="custom value 1",
            prop2="custom value 2"
        )
        self.assertEqual(value_object_two_props.prop1, "custom value 1")
        self.assertEqual(value_object_two_props.prop2, "custom value 2")

    def test_convert_to_str(self) -> None:
        value_object_one_prop = StubOneProp(prop="custom value")
        self.assertEqual(value_object_one_prop.prop, str(value_object_one_prop))

        value_object_two_props = StubTwoProps(
            prop1="message 1",
            prop2="message 2"
        )
        self.assertEqual('{"prop1": "message 1", "prop2": "message 2"}', str(value_object_two_props))

    def test_is_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            value_object = StubOneProp(prop="custom value")
            value_object.prop = "custom modified"

class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self) -> None:
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self) -> None:
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:
            with self.assertRaises(InvalidUuidException) as assert_error:
                UniqueEntityId("fake id")
            mock_validate.assert_called_once()
            self.assertEqual(assert_error.exception.args[0], "ID must be a valid UUID")

    def test_accept_uuid_passed_in_constructor(self) -> None:
        with (patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate):
            value_object = UniqueEntityId("e3201cad-6d42-4aa0-b0bf-603280c10d15")
            mock_validate.assert_called_once()
            self.assertEqual(value_object.id, "e3201cad-6d42-4aa0-b0bf-603280c10d15")

        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_no_passed_id_in_constructor(self) -> None:
        with (patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate):
            value_object = UniqueEntityId()
            mock_validate.assert_called_once()
            self.assertIsNotNone(value_object.id)
            self.assertTrue(uuid.UUID(value_object.id))

    def test_is_immutable(self) -> None:
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "fake id"
