import importlib
from graphios_ng.utils import with_log
from graphios_ng.configurable import Configurable


class Parser(Configurable):
    required_config = []

    @with_log
    def __init__(self, config, log=None):
        super(Parser, self).__init__(config)

    @with_log
    def parse_host_perfdata(self, path, log=None):
        log.debug('Parsing host perfdata from file %s' % path)

    @with_log
    def parse_service_perfdata(self, path, log=None):
        log.debug('Parsing service perfdata from file %s' % path)


class FileParser(Parser):
    def __init__(self, config):
        super(FileParser, self).__init__(config)

    @with_log
    def _parse_host_perfline(self, line, log=None):
        pass

    @with_log
    def _parse_service_perfline(self, line, log=None):
        pass

    @with_log
    def parse_host_perfdata(self, path, log=None):
        super(FileParser, self).parse_host_perfdata(path)

        with open(path, 'r') as datafile:
            return [self._parse_host_perfline(line) for line in datafile]

    @with_log
    def parse_service_perfdata(self, path, log=None):
        super(FileParser, self).parse_service_perfdata(path)

        with open(path, 'r') as datafile:
            return [self._parse_service_perfline(line) for line in datafile]


@with_log
def create_parser(config, log=None):
    if 'type' not in config:
        log.error('Missing type for parser in config: %s' % config)
        return None

    try:
        module_name = 'graphios_ng.parser.%s' % config['type']
        module_parts = config['type'].split('_')
        class_parts = [parts.capitalize() for parts in module_parts]
        class_name = '%sParser' % ''.join(class_parts)
        log.debug('Trying to create %s from module %s' %
                  (class_name, module_name))

        module = importlib.import_module(module_name)
        output = getattr(module, class_name)
        return output(config)

    except ImportError as error:
        log.error('Could not import %s: %s' % (module_name, error))
        return None
