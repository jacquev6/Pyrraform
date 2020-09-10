from typing import Dict, NoReturn, Type
import os
import sys
import logging
import concurrent.futures
import datetime
import socket
import textwrap
import uuid
import abc

import grpc
import cryptography.hazmat.primitives.asymmetric.rsa
import umsgpack

from . import tfplugin5_0_pb2
from . import tfplugin5_0_pb2_grpc
from . import grpc_controller_pb2
from . import grpc_controller_pb2_grpc


logging.basicConfig(
    filename="/terraform-provider-pyrraform-test.log",
    level=logging.INFO,
    format="{asctime}.{msecs:03.0f}:{levelname}:{name}:{message}",
    style="{",
    datefmt="%Y%m%d-%H%M%S",
)

log = logging.getLogger(__name__)


class Schema:
    # @todo Generate tfplugin5_0_pb2.Schema from structured definition instead of storing it
    # Type system:
    # https://github.com/zclconf/go-cty/blob/4e1b2a3ccc87ef459dac0e425f139c117a2d790f/cty/json.go#L16

    # @todo Understand the difference between `required` and `optional` fields
    # Hypothesis: `required` means the attribute must appear in the config file
    # and `optional` allows the attribute to be absent from self.read's return value

    # @todo Understand the `computed` field

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


def run_provider(provider_class: Type[Provider]) -> NoReturn:
    # @todo Understand why terraform starts and stops the plugin several times
    # For example, when running "terraform refresh" on a config with just a single data source:
    # - GetSchema, Shutdown
    # - GetSchema, PrepareProviderConfig, ValidateDataSourceConfig, Shutdown
    # - GetSchema, Configure, ValidateDataSourceConfig, ReadDataSource, Shutdown
    # - GetSchema, Configure, Shutdown
    # - GetSchema, Configure, Shutdown
    # I would assume starting the plugin once and calling GetSchema, PrepareProviderConfig,
    # Configure, ValidateDataSourceConfig, ReadDataSource, Shutdown would be enough.
    # Note that the PLUGIN_CLIENT_CERT changes.
    log.info(f"Enter main with command-line {sys.argv}")
    for k, v in os.environ.items():
        log.debug(f"Environment variable: {k}={v}")

    (certificate, private_key) = generate_certificate()
    log.debug(f"Server certificate: {certificate.decode('utf-8')}")
    with open("provider-pyrraform-test.cert.pem", "wb") as f:
        f.write(certificate)
    raw_base64_certificate = ''.join(certificate.decode('utf-8').splitlines()[1:-1]).rstrip("=")

    if os.environ.get("TF_PLUGIN_MAGIC_COOKIE") != "d602bf8f470bc67ca7faa0386276bbdd4330efaf76d1a219cb4d6991ca9872b2":
        print(
            textwrap.dedent("""\
                This Python program is a Terraform plugin. These are not meant to be executed directly.
                Please execute terraform, which will load any plugins automatically\
            """),
            file=sys.stderr,
        )
        exit(1)

    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))

    grpc_controller_pb2_grpc.add_GRPCControllerServicer_to_server(GRPCControllerServicer(server), server)

    program_name = os.path.basename(sys.argv[0])
    assert program_name.startswith("terraform-provider-"), sys.argv
    prefix = program_name[19:]
    tfplugin5_0_pb2_grpc.add_ProviderServicer_to_server(ProviderServicer(prefix, provider_class), server)

    # @todo Support Windows by using a TCP socket
    assert sys.platform not in ["win32", "cygwin"]
    assert os.path.isdir("/tmp")
    socket_domain = "unix"
    socket_name = f"/tmp/pyrraform-{uuid.uuid4().hex}"
    server.add_secure_port(
        f"unix://{socket_name}",
        grpc.ssl_server_credentials(
            [(private_key, certificate)],
            root_certificates=os.environ["PLUGIN_CLIENT_CERT"],
            require_client_auth=True,
        ),
    )

    server.start()
    log.info("Server started")
    handshake = f"1|5|{socket_domain}|{socket_name}|grpc|{raw_base64_certificate}"
    log.debug(f"Handshake: '{handshake}'")
    print(handshake, flush=True)

    server.wait_for_termination()

    log.info("Exit main")


def generate_certificate():
    # @todo Tweak the generated cert to match the one generated by the Terraform SDK
    one_day = datetime.timedelta(1, 0, 0)
    private_key = cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=cryptography.hazmat.backends.default_backend())
    public_key = private_key.public_key()

    builder = cryptography.x509.CertificateBuilder()
    builder = builder.subject_name(cryptography.x509.Name([cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.COMMON_NAME, socket.gethostname())]))
    builder = builder.issuer_name(cryptography.x509.Name([cryptography.x509.NameAttribute(cryptography.x509.oid.NameOID.COMMON_NAME, socket.gethostname())]))
    builder = builder.not_valid_before(datetime.datetime.today() - one_day)
    builder = builder.not_valid_after(datetime.datetime.today() + (one_day*365*5))
    builder = builder.serial_number(cryptography.x509.random_serial_number())
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        cryptography.x509.SubjectAlternativeName([
            cryptography.x509.DNSName(socket.gethostname()),
            cryptography.x509.DNSName('*.%s' % socket.gethostname()),
            cryptography.x509.DNSName('localhost'),
            cryptography.x509.DNSName('*.localhost'),
        ]),
        critical=False)
    builder = builder.add_extension(cryptography.x509.BasicConstraints(ca=True, path_length=None), critical=True)

    certificate = builder.sign(
        private_key=private_key, algorithm=cryptography.hazmat.primitives.hashes.SHA256(),
        backend=cryptography.hazmat.backends.default_backend())

    return (
        certificate.public_bytes(cryptography.hazmat.primitives.serialization.Encoding.PEM),
        private_key.private_bytes(
            cryptography.hazmat.primitives.serialization.Encoding.PEM,
            cryptography.hazmat.primitives.serialization.PrivateFormat.PKCS8,
            cryptography.hazmat.primitives.serialization.NoEncryption(),
        ),
    )


class GRPCControllerServicer(grpc_controller_pb2_grpc.GRPCControllerServicer):
    def __init__(self, server):
        self.__server = server

    def Shutdown(self, request, context):
        log.info("Shutdown")
        self.__server.stop(grace=0.5)
        return grpc_controller_pb2.Empty()


class ProviderServicer(tfplugin5_0_pb2_grpc.ProviderServicer):
    def __init__(self, prefix, provider_class):
        self.__provider_class = provider_class
        self.__data_source_classes = {
            f"{prefix}_{name}": data_source_class
            for (name, data_source_class) in provider_class.data_source_classes.items()
        }
        self.__provider = None

    def GetSchema(self, request, context):
        log.info("GetSchema")
        return tfplugin5_0_pb2.GetProviderSchema.Response(
            provider=self.__provider_class.config_schema.pb_schema,
            resource_schemas={},
            data_source_schemas={
                full_name: data_source_class.config_schema.pb_schema
                for (full_name, data_source_class) in self.__data_source_classes.items()
            },
        )

    def PrepareProviderConfig(self, request, context):
        log.info(f"PrepareProviderConfig: {request}")
        config = umsgpack.unpackb(request.config.msgpack)

        prepared_config = self.__provider_class.prepare_config(config)
        self.__provider = self.__provider_class(prepared_config)

        return tfplugin5_0_pb2.PrepareProviderConfig.Response(
            prepared_config=tfplugin5_0_pb2.DynamicValue(
                msgpack=umsgpack.packb(prepared_config),
            ),
        )

    def Configure(self, request, context):
        log.info(f"Configure: {request}")
        prepared_config = umsgpack.unpackb(request.config.msgpack)

        self.__provider = self.__provider_class(prepared_config)

        return tfplugin5_0_pb2.Configure.Response()

    def ValidateDataSourceConfig(self, request, context):
        log.info(f"ValidateDataSourceConfig: {request}")
        assert self.__provider is not None
        data_source_class = self.__data_source_classes[request.type_name]
        config = umsgpack.unpackb(request.config.msgpack)

        assert data_source_class.validate_config(self.__provider, config)

        return tfplugin5_0_pb2.ValidateDataSourceConfig.Response()

    def ReadDataSource(self, request, context):
        log.info(f"ReadDataSource: {request}")
        assert self.__provider is not None
        data_source_class = self.__data_source_classes[request.type_name]
        config = umsgpack.unpackb(request.config.msgpack)

        data_source = data_source_class(self.__provider, config)
        data = data_source.read()

        return tfplugin5_0_pb2.ReadDataSource.Response(
            state=tfplugin5_0_pb2.DynamicValue(
                msgpack=umsgpack.packb(data),
            ),
        )
