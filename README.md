# avg-reading

Publish average value of stream of instantaneous readings.

Subscribe to an MQTT topic that monitors temperature (e.g. refrigerator temperature) and republish a moving average. Potential other use is average energy usage for appliances.

## Motivation

Normal temperature variation makes it difficult to set an alarm from instantaneous readings. Energy readings tend to be on/off of stair step (during defrost cycle.)

## Background

Home automation using Home Assistant (HASS) and reading temperature using Raspberry Pi Zero Ws which publish to an MQTT broker. The period for freezer temperature is about half an hour. The period for the refrigerator is ??? (recovering from a forced defrost at the moment.) 

## Typical readings

As seen using `mosquitto_sub -v ...`

```text
HA/puyallup/kitchen/fridge_temp {"t": 1692193563, "temp": 50.9}
HA/niwot/basement/freezer_temp {"t": 1692193561, "temp": 6.574999999999999}
```

(Yes, not a good temperature for refrigeration)

## Status

Calculates average from incoming JSON data and outputs in a format suitable for importing into a spreadsheet as a CSV.

TODO: Format output as a JSON payload suitable for integration with HASS

## Functionality

* Subscribe/publish MQTT (delegate this to `mosquitto_sub` and `mosquitto_pub`)
* Parse JSON using the JSON module.
* Calculate a moving average. This could be the average of 'N' previous readings which would require storage of 'N' previous readings. Could also use a digital low pass filter that would use fixed storage.
* The period of these readings can vary but can be determined by the value of 't' in successive readings. ('t' is "UNIX time" - seconds since midnight, January 1, 1970 GMT.)

With the MQTT interfacing delegated to external programs, the core logic and JSON transcription can be handled with Python as installed.

## Plan

1. Figure out a directory structure. (Start with flat?)
1. Payload parsing (read from STDIN.)
1. Implement filter and output as JSON.
1. Tie together with `mosquitto_sub`/`mosquitto_pub`.

## exercise / test

```text
echo '{"t": 1692193563, "temp": 50.9}' | ./avg_reading.py 
echo '{"t": 1692193561, "temp": 6.574999999999999}' | ./avg_reading.py 
mosquitto_sub -t HA/niwot/basement/freezer_temp -h mqtt|./avg_reading.py 
```

Given a file with saved messages from `mosquitto_sub -v -t \# -h mqtt` output

```text
grep 'HA/niwot/basement/freezer_temp' ~/Downloads/mqtt/messages.txt| head -10| \
    cut -f 1 -d ' ' --complement|./avg_reading.py
```