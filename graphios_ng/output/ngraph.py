from graphios_ng.output import Output
from graphios_ng.utils import Template
from graphios_ng.configurable import ConfigItem

DEFAULT_HOST_PERFDATA_TEMPLATE = (
    '${host}\t${output}\t${perfdata}\t${time}\n'
)

DEFAULT_SERVICE_PERFDATA_TEMPLATE = (
    '${host}\t${service}\t${output}\t${perfdata}\t${time}\n'
)


class NgraphOutput(Output):
    config_items = [ConfigItem('host_perfdata_template',
                               default=DEFAULT_HOST_PERFDATA_TEMPLATE),
                    ConfigItem('service_perfdata_template',
                               default=DEFAULT_SERVICE_PERFDATA_TEMPLATE)]

    def _build_host_output(self, data):
        template = Template(self.config['host_perfdata_template'])
        return template.safe_substitute(**data)

    def _build_service_output(self, data):
        template = Template(self.config['service_perfdata_template'])
        return template.safe_substitute(**data)

    def output(self, data):
        line = None
        if data['type'] == 'host':
            line = self._build_host_output(data)
        elif data['type'] == 'service':
            line = self._build_service_output(data)

        if line is None:
            raise ValueError('Invalid output data: %s' % data)
