import json

from graphios_ng.parser import FileParser
from graphios_ng.utils import with_log


class JsonLineParser(FileParser):
    def __init__(self, config):
        super(JsonLineParser, self).__init__(config)

    @with_log
    def _parse_json(self, line, log=None):
        try:
            return json.loads(line)
        except ValueError as error:
            log.error('Could not parse json input: %s' % error)
            return None

    @with_log
    def _parse_host_perfline(self, line, log=None):
        super(JsonLineParser, self)._parse_host_perfline(line)
        log.debug(line)
        return self._parse_json(line)

    @with_log
    def _parse_service_perfline(self, line, log=None):
        super(JsonLineParser, self)._parse_service_perfline(line)
        log.debug(line)
        return self._parse_json(line)
