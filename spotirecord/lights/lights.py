"""This module takes care of the light controls by realizing it as a class"""
import time
import threading
from ast import literal_eval
from rpi_ws281x import Adafruit_NeoPixel, ws, Color  # important: this module needs to run on a raspberry pi
from spotirecord.config import read_config


class LightController:
    def __init__(self):
        self.light_conf = read_config()["light"]
        self.led_count = self.light_conf["led_count"]
        self.max_brightness = self.light_conf["led_brightness"]
        self.spotify_color = literal_eval(self.light_conf["spotify_color"])
        self.seeking_color = literal_eval(self.light_conf["seeking_color"])
        self.loading_color = literal_eval(self.light_conf["loading_color"])
        self.animation_thread = None
        self.strip = Adafruit_NeoPixel(self.led_count, 18, 800000, 10, False, self.max_brightness, 0)
        self.strip.begin()

    def set_ready(self):
        """Fades in the light in the spotify color."""
        self.animation_thread.join()
        self.animation_thread = None
        self.fade_in(self.spotify_color)

    def set_animation(self, mode, as_thread=True):
        """
        Sets the light signal for seeking the device

        Args:
            mode: the color to perform the animation with. Possible values: "seeking" or "loading"
            as_thread: if true, the animation will loop until the function
                      "stop_seeking" is called.
        """
        if as_thread:
            self.animation_thread = threading.Thread(target=self.start_animation_thread, args=(mode, ))
            self.animation_thread.start()
        else:
            self.fade_in(self.loading_color, wait_time_ms=5)
            self.fade_out(wait_time_ms=5)

    def stop_animation(self):
        """Stops the thread that controls the seeking light animation"""
        if self.animation_thread:
            self.animation_thread.do_run = False

    def set_error(self):
        """Sets the light to the error color"""
        if self.animation_thread:
            self.animation_thread.join()
            self.animation_thread = None
        self.fade_in((255, 0, 0), wait_time_ms=10)

    def fade_in(self, color, wait_time_ms=30):
        """Shows the desired color after fading it in.

        Args:
            color: a tuple with the values (R, G, B)
            wait_time_ms: the amount of milliseconds to wait until increasing the brightness.
        """
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

    def set_album_color(self, color):
        self.animation_thread.join()
        self.animation_thread = None
        self.fade_in(color)

    def start_animation_thread(self, mode):
        t = threading.currentThread()
        if mode == "seeking":
            color = self.seeking_color
        else:
            color = self.loading_color
        while getattr(t, "do_run", True):
            self.fade_in(color, wait_time_ms=5)
            self.fade_out(wait_time_ms=5)

    def cleanup(self):
        """Turns off all LEDs of the stripe."""
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0))
        self.strip.show()
