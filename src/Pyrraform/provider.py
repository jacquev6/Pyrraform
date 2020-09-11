from typing import Dict, Type
import abc

from . import tfplugin5_0_pb2


class Schema:
    # @todo Generate tfplugin5_0_pb2.Schema from structured definition instead of storing it
    # Type system:
    # https://github.com/zclconf/go-cty/blob/4e1b2a3ccc87ef459dac0e425f139c117a2d790f/cty/json.go#L16

    # @todo Understand the difference between `required` and `optional` fields
    # Hypothesis: `required` means the attribute must appear in the config file
    # and `optional` allows the attribute to be absent from self.read's return value

    # @todo Understand the `computed` field

    # @todo Check for reserved attribute names
    # More generaly, provide a function like terraform-plugin-sdk's InternalValidate, that
    # "should be called in a unit test [...] to verify [...] that a resource is properly configured"

    # @todo Double-check that "One of [optional or required] must be set if the value is not
    # computed. That is: value either comes from the config, is computed, or is both."
    _empty_pb_schema = tfplugin5_0_pb2.Schema(
        block=tfplugin5_0_pb2.Schema.Block(
            attributes=[],
            block_types=[],
        )
    )

    def __init__(self, pb_schema=_empty_pb_schema):
        self.pb_schema = pb_schema


class DataSource(abc.ABC):
    config_schema: Schema = Schema()
    # @todo Split config schema and output schema?

    @classmethod
    def validate_config(cls, provider: "Provider", config: Dict) -> bool:
        return True

    def __init__(self, provider: "Provider", config: Dict):
        self._provider = provider
        self._config = config

    @abc.abstractmethod
    def read(self) -> dict:
        pass


class Provider:
    config_schema: Schema = Schema()

    data_source_classes: Dict[str, Type[DataSource]] = {}

    @classmethod
    def prepare_config(self, config: Dict) -> Dict:
        return config

    def __init__(self, prepared_config: Dict):
        self._config = prepared_config
