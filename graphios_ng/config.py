import argparse
import os
import yaml
import logging

from graphios_ng.utils import with_log


class Config():
    config = {
        'dry_run': False,
        'logging': None,
        'inputs': [],
        'outputs': []
    }

    def __init__(self, path=None):
        logging.basicConfig()

        if path and os.path.exists(path):
            self.load_config(path)
        self.parse_args()

    def load_config(self, path):
        data = dict()
        with open(path, 'r') as configfile:
            data = yaml.load(configfile)

        for key in self.config.keys():
            if key in data:
                self.config[key] = data[key]

        if self.logging is not None:
            logging.config.dictConfig(self.logging)

    @with_log
    def parse_args(self, log=None):
        parser = argparse.ArgumentParser()

        parser.add_argument('-v', '--verbose', action='store_true',
                            dest='verbose', default=argparse.SUPPRESS,
                            help='log DEBUG messages')
        parser.add_argument('-n', '--dry-run', action='store_true',
                            dest='dry_run', default=argparse.SUPPRESS,
                            help='do not delete processed files and do ' +
                                 'not really send the data to graphite')
        parser.add_argument('-c', '--config', metavar='CONFIG',
                            dest='config', default=argparse.SUPPRESS,
                            help='yaml config file path')
        args = parser.parse_args()

        if 'config' in args:
            self.load_config(args.config)

        if 'verbose' in args:
            logging.getLogger().setLevel(logging.DEBUG)

        if 'dry_run' in args:
            self.config['dry_run'] = args.dry_run

        log.debug("Starting with this config: %s" % self.config)

    @with_log
    def __getattr__(self, attr, log=None):
        return getattr(self.config, attr)
