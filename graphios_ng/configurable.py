from graphios_ng.utils import with_log


class Configurable(object):
    required_config = []

    @with_log
    def __init__(self, config, log=None):
        self.config = config
        log.debug('Creating %s with config: %s' %
                  (self.__class__.__name__, config))

        for elem in self.required_config:
            if elem not in config:
                raise ValueError('Missing required configuration item: %s' %
                                 elem)

    def get_config(self, key, default=None):
        if key in self.config:
            return self.config[key]
        return default
