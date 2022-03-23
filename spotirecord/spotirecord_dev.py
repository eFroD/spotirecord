"""A testing runnable for pre_nfc-versions as a command line tool"""
import time

from spotirecord.lights import LightController
from spotirecord.client import Player
from spotirecord.image import get_best_color
from spotirecord.nfc import ntag


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


def start_album(url, player, light_controller):
    print("Starting...")
    light_controller.set_animation("loading")
    player.play_album(url)
    cover = player.get_album_cover()
    best_colors = get_best_color(cover)
    light_controller.stop_animation()
    light_controller.set_album_color(best_colors)


def run():
    print("Spotirecord starting.")
    print("Initialize Light controller...")
    light_controller = LightController()
    # just in case...
    light_controller.cleanup()
    try:
        print("Looking for device")
        light_controller.set_animation("seeking")
        player = seek_device(light_controller)
        print("Connected to device! We're ready to go!")
        try:
            while True:
                url = ntag.read_tag()
                if url and url != player.current_url:
                    print("Should start playing")
                    player.current_url = url
                    start_album(url, player, light_controller)
                if not url and not player.paused:
                    print("Url not found, trying again.")
                    url = ntag.read_tag()
                    if not url:
                        print("Okay, tag is gone, should pause here.")
                        player.current_url = None
                        player.pause_playback_api()
                        light_controller.set_ready()

        except KeyboardInterrupt:
            player.pause_playback()
    finally:
        if light_controller.animation_thread:
            light_controller.stop_animation()
        light_controller.cleanup()
        ntag.cleanup()
