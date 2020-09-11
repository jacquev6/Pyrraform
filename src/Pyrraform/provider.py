from typing import Dict, Type
import abc
import json

from . import tfplugin5_0_pb2
from . import schema


class DataSource(abc.ABC):
    config_schema: schema.Schema = schema.empty
    # @todo Split config schema and output schema?

    # @todo Check for reserved attribute names in config_schema
    # More generaly, provide functions like terraform-plugin-sdk's InternalValidate, that
    # "should be called in a unit test [...] to verify [...] properly configured"

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
    config_schema: schema.Schema = schema.empty

    data_source_classes: Dict[str, Type[DataSource]] = {}

    @classmethod
    def prepare_config(self, config: Dict) -> Dict:
        return config

    def __init__(self, prepared_config: Dict):
        self._config = prepared_config
