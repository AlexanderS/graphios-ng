import importlib
import os
import pyinotify

from graphios_ng.utils import with_log
from graphios_ng.configurable import ConfigItem, Configurable


class Parser(Configurable):
    def __init__(self, config, handler):
        self.handler = handler
        super(Parser, self).__init__(config)

    @with_log
    def parse_host_perfdata(self, path, log=None):
        log.debug('Parsing host perfdata from file %s' % path)

    @with_log
    def parse_service_perfdata(self, path, log=None):
        log.debug('Parsing service perfdata from file %s' % path)

    def handle_data(self, data):
        self.handler.handle_data(data)


class FileNotifier(pyinotify.ProcessEvent):
    def __init__(self, path, handler):
        pyinotify.ProcessEvent.__init__(self)
        self.handler = handler

        # initial files
        files = os.listdir(path)
        for filename in files:
            self.handler(os.path.join(path, filename))

        # inotify for new files
        wm = pyinotify.WatchManager()
        mask = (pyinotify.IN_CLOSE_WRITE |  # pylint: disable=E1101
                pyinotify.IN_MOVED_TO)  # pylint: disable=E1101
        pyinotify.AsyncNotifier(wm, self)
        wm.add_watch(path, quiet=False, mask=mask)

    def process_IN_CLOSE_WRITE(self, event):
        self.handler(event.pathname)

    def process_IN_MOVED_TO(self, event):
        self.handler(event.pathname)


class FileParser(Parser):
    config_items = [ConfigItem('path', required=True)]

    def __init__(self, config, handler):
        super(FileParser, self).__init__(config, handler)

        FileNotifier(os.path.realpath(self.config['path']),
                     self.handle_file)

    def handle_file(self, path):
        filename = os.path.basename(path)
        if filename.startswith('host-perfdata.'):
            self.parse_host_perfdata(path)
        elif filename.startswith('service-perfdata.'):
            self.parse_service_perfdata(path)

    def _parse_host_perfline(self, _line, log=None):
                # pylint: disable=W0613
        return {
            'type': 'host',
            'host': None,
            'output': None,
            'perfdata': None,
            'time': None,
            'graphios_template': None
        }

    def _parse_service_perfline(self, _line, log=None):
                # pylint: disable=W0613
        return {
            'type': 'service',
            'host': None,
            'service': None,
            'output': None,
            'perfdata': None,
            'time': None,
            'graphios_template': None
        }

    @with_log
    def parse_host_perfdata(self, path, log=None):
        super(FileParser, self).parse_host_perfdata(path)

        with open(path, 'r') as datafile:
            for line in datafile:
                self.handle_data(self._parse_host_perfline(line))

    @with_log
    def parse_service_perfdata(self, path, log=None):
        super(FileParser, self).parse_service_perfdata(path)

        with open(path, 'r') as datafile:
            for line in datafile:
                self.handle_data(self._parse_service_perfline(line))


@with_log
def create_parser(config, handler, log=None):
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
        return output(config, handler)

    except ImportError as error:
        log.error('Could not import %s: %s' % (module_name, error))
        return None
