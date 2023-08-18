#!/usr/bin/env python3
""" code to implement all functionality """

import sys
import json

def parse_line(line):
    """ parse timestamp and temperature from input """
    try:
        fields = json.loads(line)
        # do the fields exist in the JSON?
        if "t" not in fields or "temp" not in fields:
            return (-1, "")
    # Error parsing JSON
    except ValueError:
        print("Cannot decode '{}'".format(line.strip("\n")), file=sys.stderr)
        return (-1, "")
    return (fields["t"], fields["temp"])

# Python - no static variable in functions :-/
accumulator = 0     # accumulator for average
index = 0           # index of next slot in array of values
values = []         # stored values
count = 0           # number of values stored
VALUE_COUNT = 60    # number of values to store

for i in range(VALUE_COUNT):
    values.append(0)

def average(val):
    """ calculate running average from sample """
    global accumulator 
    global index
    global values
    global count
    global VALUE_COUNT

    accumulator -= values[index]  # subtract out previous value
    accumulator += val  # add in new value
    values[index] = val  # store new value
    index += 1  # index next slot
    if index >= VALUE_COUNT:    # roll over
        index = 0
    if count < VALUE_COUNT:
        count += 1
    return accumulator/count

def main():
    """ main entry point """
    for line in sys.stdin:
        (timestamp, temperature) = parse_line(line)
        avg = average(temperature)
        print(json.dumps({"t":timestamp, "temp":temperature, "average":avg}))


if __name__ == '__main__':
    main()
