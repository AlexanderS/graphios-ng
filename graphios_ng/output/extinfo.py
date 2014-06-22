import os

from graphios_ng.configurable import ConfigItem
from graphios_ng.output import Output
from graphios_ng.utils import get_valid_filename, Template


DEFAULT_HOST_MARKER = '# ExtInfo for ${host}'

DEFAULT_HOST_TEMPLATE = (
    '''
define hostextinfo {
    host_name            ${host}
    icon_image           nagiosgrapher/dot.png' alt='' border='0'></a>'''
    '''<a href='graphs.cgi?host={host}'>'''
    '''<img src='rrd2-system.cgi?host=${host}&start=-5400&end=now'''
    '''&title=Actual&width=20&height=20&type=AVERAGE&only-graph=true'
}''')

DEFAULT_SERVICE_MARKER = '# ExtInfo for ${service} on ${host}'

DEFAULT_SERVICE_TEMPLATE = (
    '''
define serviceextinfo {
    host_name            ${host}
    icon_image           nagiosgrapher/dot.png' alt='' border='0'></a>'''
    '''<a href='graphs.cgi?host=${host|urlencode}'''
    '''&service=${service|urlencode}'>'''
    '''<img src='rrd2-system.cgi?host=${host|urlencode}'''
    '''&service=${service|urlencode}'''
    '''&start=-5400&end=now&title=Actual&width=20&height=20'''
    '''&type=AVERAGE&only-graph=true'
    service_description  ${service}
}
''')


class ExtinfoOutput(Output):
    config_items = [ConfigItem('filename', required=True),
                    ConfigItem('host_marker',
                               default=DEFAULT_HOST_MARKER),
                    ConfigItem('host_template',
                               default=DEFAULT_HOST_TEMPLATE),
                    ConfigItem('service_marker',
                               default=DEFAULT_SERVICE_MARKER),
                    ConfigItem('service_template',
                               default=DEFAULT_SERVICE_TEMPLATE)]

    def _write(self, filename, elem):
        marker = self._build_marker(elem)
        with open(filename, 'a+') as output:
            for line in output:
                if line.rstip() == marker.rstrip():
                    return

            content = self._build_content(elem)
            output.write('\n')
            output.write(marker)
            output.write(content)

    def _build_content(self, elem):
        if 'service' in elem:
            template = self.config['service_template']
        else:
            template = self.config['host_template']
        return Template(template).safe_substitute(**elem)

    def _build_path(self, elem):
        was_absolute = os.path.isabs(self.config['filename'])
        templates = self.config['filename'].split(os.sep)
        parts = [get_valid_filename(Template(template).safe_substitute(**elem))
                 for template in templates]
        path = os.path.join(*parts)
        if was_absolute:
            return os.sep + path
        return path

    def _create_directory(self, path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _build_marker(self, elem):
        if 'service' in elem:
            marker = self.config['service_marker']
        else:
            marker = self.config['host_marker']
        return Template(marker).safe_substitute(**elem)

    def _handle_elem(self, elem):
        path = self._build_path(elem)

        if not os.path.exists(path):
            self._create_directory(path)
        self._write(path, elem)

    def output(self, data):
        for elem in data:
            self._handle_elem(elem)
