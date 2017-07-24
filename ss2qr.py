#!/usr/bin/env python3

import json
import pyqrcode
import ss2uri
import sys


class TerminalPrinter:

    def __enter__(self):
        sys.stdout.buffer.write(b'\x1b[38;5;16m\x1b[48;5;231m')
        self.last_line = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.flush()
        sys.stdout.buffer.write(b'\x1b[39m\x1b[49m\n\n')

    def write(self, line=[]):
        if self.last_line is None:
            self.last_line = line
        else:
            last_line = self.last_line
            self.last_line = None
            sys.stdout.buffer.write(b'\n')
            for i in range(max(len(last_line), len(line))):
                upper_pixel = last_line[i] if i < len(last_line) else 0
                lower_pixel = line[i] if i < len(line) else 0
                sys.stdout.buffer.write((('\u0020', '\u2584'), ('\u2580', '\u2588'))[upper_pixel][lower_pixel].encode('utf-8'))

    def flush(self):
        if self.last_line is not None:
            self.write()


def main(argv):
    if len(argv) == 1:
        print('Usage: {} config.json'.format(argv[0]))
        print()
    with TerminalPrinter() as term:
        for c in range(3):
            term.write()
        for i in argv[1:]:
            with open(i, 'r', encoding='utf-8', errors='replace') as f:
                conf = dict(json.load(f))
                uri = ss2uri.ss2uri(conf)
                qr = pyqrcode.create(uri, error='L')
                for line in qr.code:
                    term.write([0] * ((80 - len(line)) // 2) + line)
            for c in range(3):
                term.write()


if __name__ == '__main__':
    main(sys.argv)
