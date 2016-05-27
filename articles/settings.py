import logging
import yaml


def _get_settings():
    with(open('./config.yaml', 'r')) as f:
        settings = yaml.load(f.read())
        return settings['dev']


settings = _get_settings()
