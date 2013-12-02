import argparse
import os
import yaml
import logging

from graphios_ng.utils import with_log


class ConfigItem(object):
    def __init__(self, defaults):
        self.defaults = defaults
        self.values = dict()

    def set(self, config):
        for (key, value) in config.items():
            if (key in self.defaults and
                    isinstance(self.defaults[key], self.__class__)):
                self.defaults[key].set(value)
            else:
                self.defaults[key] = value

    def __getattr__(self, attr):
        if attr in self.values:
            return self.values[attr]
        return self.defaults[attr]

    def __repr__(self):
        config = self.defaults
        for (key, value) in self.values.items():
            config[key] = value
        return config.__repr__()


class Config():
    config = ConfigItem({
        'carbon': ConfigItem({
            'host': 'localhost',
            'port': 2004,
            'max_sleep': 30
        }),

        'spool_dir': '/var/spool/graphite/',
        'dry_run': False,
        'logging': None
    })

    def __init__(self, path=None):
        logging.basicConfig()

        if path and os.path.exists(path):
            self.load_config(path)
        self.parse_args()

    def load_config(self, path):
        with open(path, 'r') as configfile:
            self.config.set(yaml.load(configfile))

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
        parser.add_argument('-s', '--spool-directory',
                            metavar='DIR', dest='spool_dir',
                            default=argparse.SUPPRESS,
                            help='directory to scan for performance data')
        args = parser.parse_args()

        if 'config' in args:
            self.load_config(args.config)

        if 'verbose' in args:
            logging.getLogger().setLevel(logging.DEBUG)

        self.config.set({key: getattr(args, key)
                         for key in ['dry_run', 'spool_dir']
                         if key in args})

        log.debug("Starting with this config: %s" % self.config)

    @with_log
    def __getattr__(self, attr, log=None):
        return getattr(self.config, attr)
