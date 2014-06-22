from graphios_ng.configurable import ConfigItem
from graphios_ng.output import Output
from graphios_ng.utils import Template


class StdoutOutput(Output):
    config_items = [ConfigItem('host_template'),
                    ConfigItem('service_template')]

    def __init__(self, config):
        self['host_template'] = 'Host: ${_data}'
        self['service_template'] = 'Service: ${_data}'
        super(StdoutOutput, self).__init__(config)

    def __call__(self, data):
        data['_data'] = data

        if data['type'] == 'host':
            print(Template(self['host_template']).safe_substitute(**data))
        elif data['type'] == 'service':
            print(Template(self['service_template']).safe_substitute(**data))
        else:
            print('Unknown entry parsed.')
