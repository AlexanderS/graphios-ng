import os
import pyinotify
import signal
import sys

from graphios_ng.carbon import CarbonConnection
from graphios_ng.config import Config
from graphios_ng.utils import with_log
from graphios_ng import asynsched


class Graphios(pyinotify.ProcessEvent):
    def __init__(self):
        pyinotify.ProcessEvent.__init__(self)

        self.config = Config()
        self.carbon = CarbonConnection(self.config.carbon.host,
                                       self.config.carbon.port,
                                       self.config.carbon.max_sleep)
        self.spool_dir = os.path.realpath(self.config.spool_dir)

        # initial files
        files = os.listdir(self.spool_dir)
        for filename in files:
            self.handle_file(os.path.join(self.spool_dir, filename))

        # inotify for new files
        wm = pyinotify.WatchManager()
        mask = (pyinotify.IN_CLOSE_WRITE |  # pylint: disable=E1101
                pyinotify.IN_MOVED_TO)  # pylint: disable=E1101
        pyinotify.AsyncNotifier(wm, self)
        wm.add_watch(self.spool_dir, quiet=False, mask=mask)

    @with_log
    def handle_file(self, path, log=None):
        filename = os.path.basename(path)
        if filename.startswith('host-perfdata.'):
            log.debug('Processing host performance data from %s' % path)
        elif filename.startswith('service-perfdata.'):
            log.debug('Processing service performance data from %s' % path)

    def process_IN_CLOSE_WRITE(self, event):
        self.handle_file(event.pathname)

    def process_IN_MOVED_TO(self, event):
        self.handle_file(event.pathname)


def main():
    Graphios()

    # mainloop until interrupt
    signal.signal(signal.SIGTERM, (lambda signal, frame: sys.exit(0)))
    try:
        asynsched.loop()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    sys.exit(0)
