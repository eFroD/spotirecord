"""A testing runnable for pre_nfc-versions as a command line tool"""
import time

from spotirecord.lights import LightController
from spotirecord.client import Player


def seek_device(light_controller):
    """Tries to obtain the specified device"""
    for i in range(15):
        try:
            player = Player()
            light_controller.stop_animation()
            light_controller.set_ready()
            return player
        except TypeError:
            print(f"Still waiting for device. Attempt: {i+1}")
            time.sleep(1)

    light_controller.stop_animation()
    light_controller.set_error()
    raise ConnectionError("The device could not be found!\n"
                          "Make sure that you have provided the correct name and that the client is opened.")


def run():
    print("Spotirecord starting.")
    print("Initialize Light controller...")
    light_controller = LightController()
    # just in case...
    light_controller.cleanup()
    print("Looking for device")
    light_controller.set_animation("seeking")
    player = seek_device(light_controller)
    print("Connected to device! We're ready to go!")
    print("Features:")
    print("Paste a spotify URL to play an album.")
    print("Type \"pause\" to pause the playback and \"resume\" to resume")
    try:
        while True:
            url = input("Your turn: ")
            if url == "resume":
                print("resuming...")
                player.play_album(resume=True)
            elif url == "pause":
                print("pausing.")
                player.pause_playback()
            else:
                print("Starting...")
                player.play_album(url)
    except KeyboardInterrupt:
        light_controller.cleanup()
        player.pause_playback()

