"""This module handles playback of albums and music controls."""
import requests
import keyboard
from spotirecord import client
from spotirecord.client import utils

PAUSE_KEY = 172


class Player:
    """
    This class is used to control the functions needed for playing music.

    Attributes:
         device: The device ID.
    """
    def __init__(self):
        self.device = client.get_device_id()
        self.current_url = None
        self.paused = True

    def play_album(self, url=None, resume=False):
        """
        Starts the playback of an URL-Given album.

        Args:
            url: the url of the album. Can be obtained when sharing the album.
            resume: if set to true, the album uri is not passed which results in just resuming the playback.
        """
        endpoint = "https://api.spotify.com/v1/me/player/play"
        access_token = client.authenticate()
        if resume:
            request_body = {}
            self.pause_playback_api()
        else:
            uri = utils.extract_uri(url)
            request_body = {"context_uri": uri}
        header = utils.create_access_header(access_token)
        playback_result = requests.put(endpoint, params={"device_id": self.device},
                                       headers=header, json=request_body)
        if playback_result.status_code == 202 or playback_result.status_code == 200:
            print("Playing.")
            self.paused = False
        else:
            raise ConnectionError(f"Connection failed. Status code: {playback_result.status_code}\n"
                                  f"Original message: {playback_result.text}")

    def pause_playback(self):
        """
        Pause the playback emulating a media keypress, instead of using the API.
        This should provide a faster experience
        """
        keyboard.send(PAUSE_KEY)
        self.paused = not self.paused

    def pause_playback_api(self):
        """Pause the running playback"""
        endpoint = "https://api.spotify.com/v1/me/player/pause"
        access_token = client.authenticate()
        header = utils.create_access_header(access_token)
        pause_result = requests.put(endpoint, params={"device_id": self.device}, headers=header)
        if pause_result.status_code == 204 or pause_result.status_code == 202:
            print("paused.")
            self.paused = True
        else:
            raise ConnectionError(f"Connection failed. Status code: {pause_result.status_code}")

    def skip(self, next_track):
        """
        Skip to next or previous track.

        Args:
            next_track: if true, it skips to the next track, if false, then it skips to the previous track
        """
        if next_track:
            endpoint = "https://api.spotify.com/v1/me/player/next"
        else:
            endpoint = "https://api.spotify.com/v1/me/player/previous"
        access_token = client.authenticate()
        header = utils.create_access_header(access_token)
        skip_result = requests.post(endpoint, headers=header, params={"device_id": self.device})
        if skip_result.status_code == 204:
            print("skipped")
        else:
            raise ConnectionError(f"Connection failed. Status code: {skip_result.status_code}\n"
                                  f"Original message: {skip_result.text}")

    @staticmethod
    def get_album_cover():
        """Returns the url of the album cover that is currently playing."""
        return client.get_current_album_cover()
