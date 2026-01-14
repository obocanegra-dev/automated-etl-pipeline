import yaml
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class PathsConfig:
    source: str
    stage: str
    archive: str
    error: str

@dataclass
class AppConfig:
    paths: PathsConfig
    aws: Dict[str, Any]
    azure: Dict[str, Any]
    sftp: Dict[str, Any]
    environment: str = "dev"

class ConfigLoader:
    def __init__(self, config_path="config/config.yaml"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> AppConfig:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found at {self.config_path}")
        
        with open(self.config_path, 'r') as f:
            raw = yaml.safe_load(f)
            
        paths = PathsConfig(**raw.get('paths', {}))
        return AppConfig(
            paths=paths,
            aws=raw.get('aws', {}),
            azure=raw.get('azure', {}),
            sftp=raw.get('sftp', {}),
            environment=raw.get('app', {}).get('environment', 'dev')
        )

    @property
    def config(self) -> AppConfig:
        return self._config

# Global instance for easy import if needed, or instantiate in main
def load_config(path=None) -> AppConfig:
    if path:
        return ConfigLoader(path).config
    # Try default relative to cwd, or relative to this file
    default_path = os.path.join(os.getcwd(), 'config', 'config.yaml')
    return ConfigLoader(default_path).config
