import os
import sys
import logging
import concurrent.futures
import datetime
import socket

import grpc
import cryptography.hazmat.primitives.asymmetric.rsa


logging.basicConfig(
    filename="/terraform-provider-pyrraform-test.log",
    level=logging.DEBUG,
    format="{asctime}.{msecs:03.0f}:{levelname}:{name}:{message}",
    style="{",
    datefmt="%Y%m%d-%H%M%S",
)

log = logging.getLogger(__name__)


def main():
    log.info(f"Enter main with command-line {sys.argv}")
    for k, v in os.environ.items():
        log.debug(f"Environment variable: {k}={v}")

    (certificate, private_key) = generate_certificate()
    log.debug(f"Server certificate: {certificate.decode('utf-8')}")
    with open("provider-pyrraform-test.cert.pem", "wb") as f:
        f.write(certificate)
    raw_base64_certificate = ''.join(certificate.decode('utf-8').splitlines()[1:-1]).rstrip("=")

    # @todo Check TF_PLUGIN_MAGIC_COOKIE

    server = grpc.server(concurrent.futures.ThreadPoolExecutor(max_workers=10))

    # @todo Generate a random name for the Unix socket to avoid collisions
    # @todo Support Windows by using a TCP socket
    server.add_secure_port(
        "unix:///tmp/test-1",
        grpc.ssl_server_credentials(
            [(private_key, certificate)],
            # @todo Use PLUGIN_CLIENT_CERT to authentify the client
            root_certificates=None,
            require_client_auth=False,
        ),
    )
    server.start()
    log.info("Server started")
    handshake = f"1|5|unix|/tmp/test-1|grpc|{raw_base64_certificate}"
    log.debug(f"Handshake: '{handshake}'")
    print(handshake, flush=True)
    server.wait_for_termination()

    log.info("Exit main")


def generate_certificate():
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
