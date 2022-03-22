#!/usr/bin/env python
"""A Module that will be used to read data from NTAGs."""

import RPi.GPIO as GPIO
import MFRC522
import signal

continue_reading = True


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
        print(f"Found UID: {uid_1}")
    print("Trying to use the id to select the tag")
    (status, uid_2) = reader.MFRC522_SelectTag(uid_1)
    if status == reader.MI_OK:
        print(f"IT WORKED, second part of uid: {uid_2}")

    else:
        print("did not work")

