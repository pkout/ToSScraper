import os
from enum import Enum
from pathlib import Path

import yaml

class Environment(Enum):
    dev = 'dev'
    test = 'test'

class Settings:

    def __init__(self, env=Environment.test):
        file_path = Path(__file__).parent.parent / \
            Path(f'settings.{env.value}.yaml')

        if not file_path.exists():
            raise ConfigurationFileNotFound(
                f'Configuration file was not found on path {file_path}!'
            )

        with open(file_path, 'r', encoding='utf-8') as f:
            self._settings_dict = yaml.safe_load(f)

    def as_dict(self):
        return self._settings_dict

    def as_current_profile_dict(self):
        return self._settings_dict['resolution'][self._settings_dict['profile']]


class ConfigurationFileNotFound(FileNotFoundError):
    pass

env = getattr(Environment, os.environ.get('ENVIRONMENT', 'test'))
settings = Settings(env=env).as_dict()
profiled_settings = Settings(env=env).as_current_profile_dict()