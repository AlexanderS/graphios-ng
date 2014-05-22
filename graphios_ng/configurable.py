from graphios_ng.utils import with_log


class Configurable(object):
    config_items = []
    _config = dict()

    @with_log
    def __init__(self, config, log=None):
        log.debug('Creating %s with config: %s' %
                  (self.__class__.__name__, config))

        for (key, required) in self.config_items:
            if key in config:
                self._config[key] = config[key]
            elif required:
                raise ValueError('Missing required configuration item: %s' %
                                 key)
            elif key not in self._config:
                self._config[key] = None

    def __getitem__(self, key):
        return self._config[key]

    def __setitem__(self, key, value):
        self._config[key] = value
