import uuid
import unittest
from abc import ABC
from dataclasses import is_dataclass, dataclass
from __seedwork.domain.entities import Entity
from __seedwork.domain.value_objects import UniqueEntityId


@dataclass(kw_only=True, frozen=True)
class StubEntity(Entity):

    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self) -> None:
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_a_abstract_class(self) -> None:
        self.assertIsInstance(Entity(), ABC)

    def test_set_unique_entity_id_and_props(self) -> None:
        entity = StubEntity(prop1="value 1", prop2="value 2")
        self.assertEqual(entity.prop1, "value 1")
        self.assertEqual(entity.prop2, "value 2")
        self.assertTrue(uuid.UUID(entity.id))
        self.assertEqual(entity.unique_entity_id.id, entity.id)
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)

    def test_accept_a_valid_uuid(self) -> None:
        entity = StubEntity(
            unique_entity_id=UniqueEntityId("82f08114-5a9e-4919-bfab-fc4daa9612f0"),
            prop1="value 1",
            prop2="value 2"
        )
        self.assertEqual(entity.id, "82f08114-5a9e-4919-bfab-fc4daa9612f0")

    def test_to_dict_method(self) -> None:
        entity = StubEntity(
            unique_entity_id=UniqueEntityId("82f08114-5a9e-4919-bfab-fc4daa9612f0"),
            prop1="value 1",
            prop2="value 2"
        )
        self.assertDictEqual(entity.to_dict(), {
            "id": "82f08114-5a9e-4919-bfab-fc4daa9612f0",
            "prop1": "value 1",
            "prop2": "value 2"
        })
