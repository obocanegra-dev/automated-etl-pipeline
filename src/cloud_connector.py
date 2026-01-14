import os
import logging
from abc import ABC, abstractmethod

# Import libraries but handle missing ones gracefully if user hasn't pip installed yet
try:
    import boto3
    from azure.storage.blob import BlobServiceClient
except ImportError:
    boto3 = None
    BlobServiceClient = None

logger = logging.getLogger(__name__)

class StorageProvider(ABC):
    @abstractmethod
    def upload_file(self, local_path: str, remote_name: str) -> bool:
        pass

class MockProvider(StorageProvider):
    def __init__(self, service_name):
        self.service_name = service_name

    def upload_file(self, local_path: str, remote_name: str) -> bool:
        logger.info(f"[MOCK] Uploading {os.path.basename(local_path)} to {self.service_name} as {remote_name}")
        return True

class S3Provider(StorageProvider):
    def __init__(self, access_key, secret_key, bucket_name, region):
        if not boto3:
            raise ImportError("boto3 not installed")
        self.bucket_name = bucket_name
        self.client = boto3.client(
            's3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region
        )

    def upload_file(self, local_path: str, remote_name: str) -> bool:
        try:
            self.client.upload_file(local_path, self.bucket_name, remote_name)
            logger.info(f"Uploaded to S3 bucket {self.bucket_name}: {remote_name}")
            return True
        except Exception as e:
            logger.error(f"S3 Upload failed: {e}")
            return False

class AzureProvider(StorageProvider):
    def __init__(self, connection_string, container_name):
        if not BlobServiceClient:
            raise ImportError("azure-storage-blob not installed")
        self.container_name = container_name
        self.service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_client = self.service_client.get_container_client(container_name)

    def upload_file(self, local_path: str, remote_name: str) -> bool:
        try:
            with open(local_path, "rb") as data:
                blob_client = self.container_client.get_blob_client(remote_name)
                blob_client.upload_blob(data, overwrite=True)
            logger.info(f"Uploaded to Azure container {self.container_name}: {remote_name}")
            return True
        except Exception as e:
            logger.error(f"Azure Upload failed: {e}")
            return False

class CloudConnectorFactory:
    @staticmethod
    def get_provider(config, provider_type) -> StorageProvider:
        if provider_type == 'aws':
            creds = config.aws
            if creds.get('access_key') == 'mock':
                return MockProvider("AWS S3")
            return S3Provider(creds['access_key'], creds['secret_key'], creds['bucket_name'], creds['region'])
        
        elif provider_type == 'azure':
            creds = config.azure
            if creds.get('connection_string') == 'mock':
                return MockProvider("Azure Blob")
            return AzureProvider(creds['connection_string'], creds['container_name'])
        
        raise ValueError(f"Unknown provider type: {provider_type}")
