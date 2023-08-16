#!/usr/bin/env python3
""" code to implement all functionality """

import sys
import json

def parse_line(line):
    """ parse timestamp and temperature from input """
    try:
        fields = json.loads(line)
    except ValueError:
        print("Cannot decode '{}'".format(line.strip("\n")), file=sys.stderr)
        return (-1, "")
    return (fields["t"], fields["temp"])


def main():
    """ main entry point """
    for line in sys.stdin:
        (timestamp, temperature) = parse_line(line)
        print("(t,temp)", timestamp, temperature)


if __name__ == '__main__':
    main()
