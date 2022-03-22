#!/usr/bin/env python
"""A Module that will be used to read data from NTAGs."""

import RPi.GPIO as GPIO
from spotirecord.nfc import MFRC522

reader = MFRC522.MFRC522()


def read_tag():
    """
    Checks if there is a tag and handels the authentication.
    If everything was successful, the tag is read and its contents are presented
    """
    (status, tagtype) = reader.MFRC522_Request(reader.PICC_REQIDL)
    if status == reader.MI_OK:
        (status, uid_1) = reader.MFRC522_Anticoll()
        if status == reader.MI_OK:
            url = _read_contents()
            return url
    return None


def _read_contents():
    """Reads the contents of the tag"""
    addresses = range(4, 40)
    data = []
    for address in addresses:
        try:
            read = reader.MFRC522_Read(address)
        except IOError:
            break
        if read:
            data.extend(["".join([chr(char) for char in read])[-4:]])
            reader.MFRC522_StopCrypto1()
    return _parse_link("".join(data))


def _parse_link(data):
    """parses the spotify album URL from the given data"""
    if "þ" in data:
        end = data.index("þ")
    else:
        end = len(data)
    return data[2:end]


def cleanup():
    GPIO.cleanup()
