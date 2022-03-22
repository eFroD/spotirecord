#!/usr/bin/env python
"""A Module that will be used to read data from NTAGs."""

import RPi.GPIO as GPIO
import MFRC522
import signal
from time import sleep
from datetime import datetime

continue_reading = True


def parse_link(data):
    """parses the spotify album URL from the given data"""
    start = "https"
    end = "þ"

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
            # data = reader.MFRC522_Read(0)
            # print(f"Read from 0, this is the data: {data}")
            # reader.MFRC522_StopCrypto1()
            # data_2 = reader.MFRC522_Read(1)
            # print(f"Read from 1, this is the data: {data_2}")
            # reader.MFRC522_StopCrypto1()
            # data_3 = reader.MFRC522_Read(2)
            # print(f"Read from 2, this is the data: {data_3}")
            # reader.MFRC522_StopCrypto1()
            addresses = range(4, 40)
            data = []
            for address in addresses:
                data.append(["".join([chr(char) for char in reader.MFRC522_Read(hex(address))])])
                reader.MFRC522_StopCrypto1()
            print(data)
    """
    status, _ = reader.MFRC522_Request(reader.PICC_REQIDL)
    if status != reader.MI_OK:
        sleep(0.1)
        continue
    status, backData = reader.MFRC522_Anticoll()
    buf = reader.MFRC522_Read(0)
    reader.MFRC522_Request(reader.PICC_HALT)
    if buf:
        print(datetime.now().isoformat(), ':'.join([hex(x) for x in buf]))


   


        if status == reader.MI_OK:
            print(f"Found UID: {uid_1}")
            print("Trying to use the id to select the tag")
            (status, uid_2) = reader.MFRC522_Anticoll()
            if status == reader.MI_OK:
                print(f"IT WORKED, second part of uid: {uid_2}")
                print("Selecting the tag.")
                uid = uid_1+uid_2
                reader.MFRC522_SelectTag(uid)
                key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
                status = reader.MFRC522_Auth(reader.PICC_AUTHENT1A, 8, key, uid)
                if status == reader.MI_OK:
                    reader.MFRC522_Read(8)
                    reader.MFRC522_StopCrypto1()
                else:
                    print("Authentication error")


            else:
                print("did not work")
"""
