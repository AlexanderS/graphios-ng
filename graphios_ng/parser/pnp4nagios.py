from graphios_ng.parser import FileParser
from graphios_ng.utils import with_log


class Pnp4nagiosParser(FileParser):
    required_config = []

    def __init__(self, config, handler):
        super(Pnp4nagiosParser, self).__init__(config, handler)

    def _check_required_keys(self, elem, keys):
        for key in keys:
            if key not in elem or elem[key] is None:
                return False
        return True

    def _parse_values(self, elem, line, translation):
        values = [value.split('::') for value in line.split('\t')]
        for (key, value) in values:
            if key in translation:
                elem[translation[key]] = value

        return elem

    @with_log
    def _parse_host_perfline(self, line, log=None):
        default = super(Pnp4nagiosParser, self)._parse_host_perfline(line)

        elem = self._parse_values(
            default, line, {
                'HOSTNAME': 'host',
                'OUTPUT': 'output',
                'HOSTPERFDATA': 'perfdata',
                'TIMET': 'time',
                'GRAPHIOSTEMPLATE': 'graphios_template'
            })

        if not self._check_required_keys(
                elem, ['host', 'perfdata', 'time']):
            raise ValueError('Missing required values in input line: %s' %
                             line)

        return elem

    @with_log
    def _parse_service_perfline(self, line, log=None):
        default = super(Pnp4nagiosParser, self)._parse_service_perfline(line)

        elem = self._parse_values(
            default, line, {
                'HOSTNAME': 'host',
                'SERVICEDESC': 'service',
                'OUTPUT': 'output',
                'HOSTPERFDATA': 'perfdata',
                'TIMET': 'time',
                'GRAPHIOSTEMPLATE': 'graphios_template'
            })

        if not self._check_required_keys(
                elem, ['host', 'service', 'perfdata', 'time']):
            raise ValueError('Missing required values in input line: %s' %
                             line)

        return elem
