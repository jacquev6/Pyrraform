import os
import sys
import time
import logging

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
        log.info(f"Environment variable: {k}={v}")
    for _ in range(20):
        log.debug("Passing some time in main")
        time.sleep(0.05)
    log.info("Exit main")
