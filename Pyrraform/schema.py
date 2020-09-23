"""
Low-level classes matching the Protobuf messages.

When possible, you should use the the higher-level classes in the
Pyrraform.configuration module. (@todo)
"""

from typing import List
from dataclasses import dataclass
import enum
import json

from .gocty import Type
from . import tfplugin5_0_pb2


@dataclass
class Attribute:
    name: str
    type: Type
    description: str
    required: bool
    optional: bool
    computed: bool
    sensitive: bool

    def to_protobuf(self):
        return tfplugin5_0_pb2.Schema.Attribute(
            name=self.name,
            type=json.dumps(self.type.to_data()).encode(),
            description=self.description,
            required=self.required,
            optional=self.optional,
            computed=self.computed,
            sensitive=self.sensitive,
        )


class NestingMode(enum.Enum):
    INVALID = 0
    SINGLE = 1
    LIST = 2
    SET = 3
    MAP = 4
    GROUP = 5


@dataclass
class NestedBlock:
    type_name: str
    block: "Block"
    nesting: NestingMode
    min_items: int
    max_items: int

    def to_protobuf(self):
        return tfplugin5_0_pb2.Schema.NestedBlock(
            type_name=self.type_name,
            block=self.block.to_protobuf(),
            nesting=self.nesting.value,
            min_items=self.min_items,
            max_items=self.max_items,
        )


@dataclass
class Block:
    version: int
    attributes: List[Attribute]
    block_types: List[NestedBlock]

    def to_protobuf(self):
        return tfplugin5_0_pb2.Schema.Block(
            version=self.version,
            attributes=[a.to_protobuf() for a in self.attributes],
            block_types=[b.to_protobuf() for b in self.block_types],
        )


@dataclass
class Schema:
    version: int
    block: Block

    def to_protobuf(self):
        return tfplugin5_0_pb2.Schema(
            version=self.version,
            block=self.block.to_protobuf(),
        )


empty = Schema(
    version=0,
    block=Block(
        version=0,
        attributes=[],
        block_types=[],
    ),
)
