import os
import logging

try:
    import paramiko
except ImportError:
    paramiko = None

logger = logging.getLogger(__name__)

class SFTPConnector:
    def __init__(self, host, port, username, password, remote_dir):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.remote_dir = remote_dir
        self.is_mock = (host == 'localhost' and password == 'password') # Simple mock check

    def upload(self, local_path: str) -> bool:
        filename = os.path.basename(local_path)
        remote_path = f"{self.remote_dir}/{filename}"

        if self.is_mock:
            logger.info(f"[MOCK] SFTP Upload {filename} -> {self.host}:{remote_path}")
            return True

        if not paramiko:
            logger.error("Paramiko not installed")
            return False

        try:
            transport = paramiko.Transport((self.host, self.port))
            transport.connect(username=self.username, password=self.password)
            sftp = paramiko.SFTPClient.from_transport(transport)
            
            sftp.put(local_path, remote_path)
            sftp.close()
            transport.close()
            logger.info(f"SFTP Upload Success: {filename}")
            return True
        except Exception as e:
            logger.error(f"SFTP Upload failed: {e}")
            return False
