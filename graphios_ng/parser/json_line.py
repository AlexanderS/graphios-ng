import json

from graphios_ng.parser import FileParser
from graphios_ng.utils import with_log


class JsonLineParser(FileParser):
    def __init__(self, config, handler):
        super(JsonLineParser, self).__init__(config, handler)

    def _parse_json(self, line, elem):
        json_line = json.loads(line)
        for key, value in json_line:
            if key not in elem or key == 'type':
                continue
            elem[key] = value
        return elem

    @with_log
    def _parse_host_perfline(self, line, log=None):
        elem = super(JsonLineParser, self)._parse_host_perfline(line)
        return self._parse_json(line, elem)

    @with_log
    def _parse_service_perfline(self, line, log=None):
        elem = super(JsonLineParser, self)._parse_service_perfline(line)
        return self._parse_json(line, elem)
