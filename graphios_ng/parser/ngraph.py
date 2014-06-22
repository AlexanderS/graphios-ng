from graphios_ng.parser import FileParser
from graphios_ng.utils import with_log


class NgraphParser(FileParser):
    def __init__(self, config, handler):
        super(NgraphParser, self).__init__(config, handler)

    def _parse_values(self, line, count):
        values = line.split('\t')
        if len(values) < count:
            raise ValueError('Invalid format of input line: %s' % line)

        return values

    @with_log
    def _parse_host_perfline(self, line, log=None):
        elem = super(NgraphParser, self)._parse_host_perfline(line)

        values = self._parse_values(line, 4)
        elem['host'] = values[0]
        elem['output'] = values[1]
        elem['perfdata'] = values[2]
        elem['time'] = values[3]
        return elem

    @with_log
    def _parse_service_perfline(self, line, log=None):
        elem = super(NgraphParser, self)._parse_service_perfline(line)

        values = self._parse_values(line, 5)
        elem['host'] = values[0]
        elem['service'] = values[1]
        elem['output'] = values[2]
        elem['perfdata'] = values[3]
        elem['time'] = values[4]
        return elem
