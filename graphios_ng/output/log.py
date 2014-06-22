import logging

from graphios_ng.configurable import ConfigItem
from graphios_ng.output import Output
from graphios_ng.utils import Template, with_log


class LogOutput(Output):
    check_level = logging._checkLevel  # pylint: disable=W0212
    config_items = [ConfigItem('level', conversion=check_level),
                    ConfigItem('host_template'),
                    ConfigItem('service_template')]

    def __init__(self, config):
        self['level'] = logging.DEBUG
        self['host_template'] = 'Host: ${_data}'
        self['service_template'] = 'Service: ${_data}'
        super(LogOutput, self).__init__(config)

    @with_log
    def __call__(self, data, log=None):
        data['_data'] = data

        if data['type'] == 'host':
            msg = Template(self['host_template']).safe_substitute(**data)
        elif data['type'] == 'service':
            msg = Template(self['service_template']).safe_substitute(**data)
        else:
            msg = 'Unknown entry.'

        log.log(self['level'], msg)
