"""This module takes care of the light controls by realizing it as a class"""
import time

from rpi_ws281x import Adafruit_NeoPixel, ws, Color  # important: this module needs to run on a raspberry pi
from spotirecord.config import read_config


class LightController:
    def __init__(self):
        self.light_conf = read_config()["light"]
        self.led_count = self.light_conf["led_count"]
        self.max_brightness = self.light_conf["led_brightness"]
        self.strip = Adafruit_NeoPixel(self.led_count, 18, 800000, 10, False, self.max_brightness, 0)
        self.strip.begin()

    def set_ready(self):
        """Fades in the light in the spotify color."""
        self.fade_in(self.light_conf["spotify_color"])

    def set_error(self):
        """Sets the light to the error color"""
        self.fade_in((255, 0, 0), wait_time_ms=10)

    def fade_in(self, color, wait_time_ms=30):
        """Shows the desired color after fading it in.

        Args:
            color: a tuple with the values (R, G, B)
            wait_time_ms: the amount of milliseconds to wait until increasing the brightness.
        """
        self.fade_out(wait_time_ms=10)
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(color[0], color[1], color[2]))
        for i in range(self.max_brightness):
            self.strip.setBrightness(i)
            self.strip.show()
            time.sleep(wait_time_ms/1000.0)

    def fade_out(self, wait_time_ms=30):
        """
        Reduce the brightness and cleanup the ligths in the end

        Args:
              wait_time_ms: the speed of the animation
        """
        for i in reversed(range(self.max_brightness)):
            self.strip.setBrightness(i)
            self.strip.show()
            time.sleep(wait_time_ms/1000.0)
        self.cleanup()

    def cleanup(self):
        """Turns off all LEDs of the stripe."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
