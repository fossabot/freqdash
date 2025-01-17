import logging
from pathlib import Path

from sshtunnel import SSHTunnelForwarder

from freqdash.core.config import RemoteFreqtradeAPI

log = logging.getLogger(__name__)


class Tunnel:
    def __init__(self, instance: RemoteFreqtradeAPI, ssh_keys_folder: Path) -> None:
        self.ssh_host = str(instance.ssh_host)
        self.ssh_port = instance.ssh_port
        self.ssh_address = f"{self.ssh_host}:{self.ssh_port}"
        self.ssh_username = instance.ssh_username
        self.ssh_pkey_filename = instance.ssh_pkey_filename
        self.ssh_password = instance.ssh_password
        self.remote_host = str(instance.remote_host)
        self.remote_port = instance.remote_port
        self.api_username = instance.api_username
        self.api_password = instance.api_password
        self.started = False
        self.local_bind_port = None

        if self.ssh_pkey_filename is None:
            self.server = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_username=self.ssh_username,
                ssh_password=self.ssh_password,
                remote_bind_address=(str(self.remote_host), self.remote_port),
            )
            log.info(
                f"Tunnel instance {self.ssh_host}:{self.ssh_port} initialised using username"
            )
        else:
            complete_path = Path(ssh_keys_folder, self.ssh_pkey_filename)
            if not complete_path.is_file():
                log.error(f"pkey cannot be found at: {complete_path}")
            else:
                log.info(f"pkey found at {complete_path}")
            self.server = SSHTunnelForwarder(
                (self.ssh_host, self.ssh_port),
                ssh_pkey=str(complete_path),
                ssh_private_key_password=self.ssh_password,
                ssh_config_file=None,
                remote_bind_address=(str(self.remote_host), self.remote_port),
            )
            log.info(
                f"Tunnel instance {self.ssh_host}:{self.ssh_port} initialised using pkey"
            )

    def start(self):
        self.server.start()
        self.local_bind_port = self.server.local_bind_port
        log.info(
            f"Tunnel started to {self.ssh_address} and locally bound to port {self.local_bind_port}"
        )

    def stop(self):
        self.server.stop()
        log.info(f"Tunnel stopped to {self.ssh_address}")
        self.local_bind_port = None
