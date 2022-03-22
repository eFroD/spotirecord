#!/usr/bin/env python
"""A Module that will be used to read data from NTAGs."""

import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
from datetime import datetime

continue_reading = True


def read_tag():
    """Reads the contents of the tag"""
    addresses = range(4, 40)
    data = []
    for address in addresses:
        read = reader.MFRC522_Read(address)
        if read:
            data.extend(["".join([chr(char) for char in read])[-4:]])
            reader.MFRC522_StopCrypto1()
    return parse_link("".join(data))


def parse_link(data):
    """parses the spotify album URL from the given data"""
    if "þ" in data:
        end = data.index("þ")
    else:
        end = len(data)
    return data[2:end]


def end_read(signal, frame):
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


signal.signal(signal.SIGINT, end_read)
reader = MFRC522.MFRC522()

print("Ntag Reader Test")
print("Press Ctrl-C to stop.")


while continue_reading:
    (status, tagtype) = reader.MFRC522_Request(reader.PICC_REQIDL)
    if status == reader.MI_OK:
        print(f"Found a Tag: {tagtype}")
        (status, uid_1) = reader.MFRC522_Anticoll()
        if status == reader.MI_OK:
            url = read_tag()
            print(url)

