import importlib

from graphios_ng.utils import with_log


class Output(object):
    @with_log
    def __init__(self, config, log=None):
        self.config = config
        log.debug('Creating %s with config: %s' %
                  (self.__class__.__name__, config))


@with_log
def create_output(config, log=None):
    if 'type' not in config:
        log.error('Missing type for output in config: %s' % config)
        return None

    try:
        module_name = 'graphios_ng.output.%s' % config['type']
        class_name = '%sOutput' % config['type'].capitalize()
        log.debug('Trying to create %s from module %s' %
                  (class_name, module_name))

        module = importlib.import_module(module_name)
        output = getattr(module, class_name)
        return output(config)

    except ImportError as error:
        log.error('Could not import %s: %s' % (module_name, error))
        return None
