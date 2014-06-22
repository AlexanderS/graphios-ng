from graphios_ng.parser import FileParser
from graphios_ng.utils import with_log


class NgraphParser(FileParser):

    def __init__(self, config):
        super(NgraphParser, self).__init__(config)
    @with_log
    def _parse_host_perfline(self, line, log=None):
        pass

    @with_log
    def _parse_service_perfline(self, line, log=None):
        pass
