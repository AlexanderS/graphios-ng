import signal
import sys

from graphios_ng.config import Config
from graphios_ng.parser import create_parser
from graphios_ng.output import create_output
from graphios_ng import asynsched


class Graphios():
    def __init__(self):
        self.config = Config()

        self.outputs = list()
        if self.config.outputs:
            for _output in self.config.outputs:
                self.outputs.append(create_output(_output))

        if self.config.inputs:
            for _input in self.config.inputs:
                create_parser(_input, self)

    def handle_data(self, data):
        for output in self.outputs:
            output(data)

    def run(self):
        asynsched.loop()


def main():
    graphios = Graphios()

    # mainloop until interrupt
    signal.signal(signal.SIGTERM, (lambda signal, frame: sys.exit(0)))
    try:
        graphios.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
    sys.exit(0)
