import os

from graphios_ng.output import Output
from graphios_ng.utils import get_valid_filename, formatter


class ExtinfoOutput(Output):
    required_config = ['dir', 'filename']

    def __init__(self, config):
        super(ExtinfoOutput, self).__init__(config)
        self.template = self.get_config(
            'template',
            '''
define serviceextinfo {{
    host_name            {host}
    icon_image           nagiosgrapher/dot.png' alt='' border='0'></a>'''
            '''<a href='graphs.cgi?host={host}&service={service}'>'''
            '''<img src='rrd2-system.cgi?host={host}&service={service}'''
            '''&start=-5400&end=now&title=Actual&width=20&height=20'''
            '''&type=AVERAGE&only-graph=true'
    service_description  {service}
}}
''')

    def _write(self, filename, content):
        with open(filename, 'a') as output:
            output.write(content)

    def _build_content(self, elem):
        return formatter.format(self.template, **elem)

    def _build_path(self, elem):
        templates = self.config['filename'].split('/')
        parts = [get_valid_filename(formatter.format(template, **elem))
                 for template in templates]
        return os.path.join(self.config['dir'], *parts)

    def _create_directory(self, path):
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def _handle_elem(self, elem):
        path = self._build_path(elem)

        if not os.path.exists(path):
            self._create_directory(path)

            # TODO: Check if extinfo allready exists in file
            self._write(path, self._build_content(elem))

    def output(self, data):
        for elem in data:
            self._handle_elem(elem)
