import asyncore
import socket
import pickle
import struct

from graphios_ng import asynsched
from graphios_ng.utils import with_log


class CarbonConnection(asyncore.dispatcher_with_send):
    @with_log
    def _init_connection(self, log=None):
        asyncore.dispatcher_with_send.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect((self.host, self.port))
        log.debug('(Re)connecting to carbon at %s:%d.' %
                  (self.host, self.port))

    def __init__(self, host, port, max_sleep=30):
        asyncore.dispatcher_with_send.__init__(self)

        self.host = host
        self.port = port
        self.reconnecting = False

        self.sleep = 1
        self.max_sleep = max_sleep
        self.reset_sleep = None

        self._init_connection()

    def _reset_sleep(self):
        def reset(con):
            con.sleep = 1
            con.reset_sleep = None

        if self.reset_sleep:
            self.reset_sleep.cancel()
        self.reset_sleep = asynsched.call_later(
            2*self.sleep,
            (lambda: reset(self)))

    def _increase_sleep(self):
        self.sleep *= 2
        if self.sleep > self.max_sleep:
            self.sleep = self.max_sleep

    def handle_error(self):
        # ignore all errors
        pass

    @with_log
    def _close(self, log=None):
        if self.connected:
            self.close()

            log.debug('Connection to carbon died. ' +
                      'Scheduling reconnect in %d seconds.' % self.sleep)
            asynsched.call_later(self.sleep, self._init_connection)
            self._reset_sleep()
            self._increase_sleep()

    def handle_close(self):
        self._close()

    @with_log
    def send_pickle(self, data, log=None):
        payload = pickle.dumps(data)
        header = struct.pack("!L", len(payload))

        log.debug('Send %d bytes to carbon.' % len(payload))
        self.out_buffer += header + payload
