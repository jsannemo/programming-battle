import io
import json
import logging

CONFIG_PATHS = ['/etc/battle/battle.conf', 'battle.conf']

# TODO: make prettier, recursive config

class Config:

    def __init__(self):
        self.web_config = {
            'debug' : False,
            'template_path' : 'battle/battle/frontend/templates'
        }
        self.problem_directory = '/opt/progbattle/installed_problems'
        self._load()

    def _load(self):
        for path in CONFIG_PATHS:
            self._load_file(path)

    def _load_file(self, path):
        try:
            with io.open(path, 'rt', encoding='UTF-8') as f:
                config = json.load(f)
        except IOError as error:
            return
        except ValueError as error:
            logging.warning('Invalid syntax in file %s: %s', path, error)
            return
        for key, value in config.items():
            if key == 'web_config':
                for k2, v2 in value.items():
                    self.web_config[k2] = v2
            else:
                setattr(self, key, value)

config = Config()
