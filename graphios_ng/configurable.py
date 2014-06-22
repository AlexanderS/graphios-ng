from collections import namedtuple

from graphios_ng.utils import with_log


class ConfigItem(namedtuple('ConfigItem', ['key', 'required',
                                           'conversion', 'default'])):
    def __new__(cls, key, required=False, conversion=None, default=None):
        return super(ConfigItem, cls).__new__(cls, key, required,
                                              conversion, default)


class Configurable(object):
    config_items = []
    config = dict()

    @with_log
    def __init__(self, config, log=None):
        log.debug('Creating %s with config: %s' %
                  (self.__class__.__name__, config))

        for config_item in self.config_items:
            if config_item.key in config:
                value = config[config_item.key]
                if config_item.conversion:
                    value = config_item.conversion(value)
                self.config[config_item.key] = value
            elif config_item.required:
                raise ValueError('Missing required configuration item: %s' %
                                 config_item.key)
            else:
                self.config[config_item.key] = config_item.default
