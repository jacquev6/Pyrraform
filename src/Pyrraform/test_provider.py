import os
import sys
import time
import logging
import socket

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
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        os.remove("/tmp/test-1")
    except FileNotFoundError:
        pass
    sock.bind("/tmp/test-1")
    sock.listen(1)
    log.info("Listening")
    print("1|5|unix|/tmp/test-1|grpc|MIICMTCCAZKgAwIBAgIRAN1XRhBbJVxM+c8cHIFaNrMwCgYIKoZIzj0EAwQwKDESMBAGA1UEChMJSGFzaGlDb3JwMRIwEAYDVQQDEwlsb2NhbGhvc3QwIBcNMjAwOTA1MTMzODEzWhgPMjA1MDA5MDYwMTM4NDNaMCgxEjAQBgNVBAoTCUhhc2hpQ29ycDESMBAGA1UEAxMJbG9jYWxob3N0MIGbMBAGByqGSM49AgEGBSuBBAAjA4GGAAQA+6vAQmkU/bBDE6l1PUm3dYl4I85k8YGeME35bnVhyaeP1Ya3mLDA+he2TJ8Gr8QhvoBuDb8bh1LaQauiaUm1v30Ber5Bz1ICdA2eACkm7nK8zaA32kHs3z72mWHEXBkrH60h5X9g5bNU10aPv/l/N2vLMkR86+5y4QBQ0jUuVeNZVw2jWDBWMA4GA1UdDwEB/wQEAwICrDAdBgNVHSUEFjAUBggrBgEFBQcDAgYIKwYBBQUHAwEwDwYDVR0TAQH/BAUwAwEB/zAUBgNVHREEDTALgglsb2NhbGhvc3QwCgYIKoZIzj0EAwQDgYwAMIGIAkIA3b31jEqTyexzBKEqrg59tzibMd2Ot+H3Xe+F7kW0uWbuvbWLO8F8Ppl1U/gzZASpP2ZlAtgOwesGI/7AJwkOg8kCQgFdhlVvSf8Jieyi2eiqfr0Z6ftPJGB/ZAO2OvgBkLXjtQCWZseH1mw8SB4Q1UwtFDEN8i4EyFARs9AkUqfFGDTGmA", flush=True)
    while True:
        connection, _ = sock.accept()
        log.info(f"Connection accepted")
        try:
            data = connection.recv(16)
            log.info(f"Data received: {data}")
        finally:
            connection.close()
    log.info("Exit main")
