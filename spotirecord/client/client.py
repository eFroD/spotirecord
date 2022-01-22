"""The client module manages the most important Spotify API related tasks."""
import requests
import json
import time

from spotirecord.config import read_config, write_client_data, read_client_data
from .authentication import authenticate
from .utils import create_access_header

conf = read_config()
client_data = read_client_data()


def get_device_id():
    """
    Retrieves the device ID according to the devicename provided in the config.

    Returns:
        The device ID that is needed for playback requests.
    """
    device_name = conf["device"]["device_name"]
    for attempt in range(3):
        device = next((item for item in _get_devices() if item["name"] == device_name), None)
        if device:
            return device["id"]
        else:
            # may occur if the player is not ready yet at startup
            print(f"Device not found at attempt {attempt+1}, trying again...")
            time.sleep(2)
    raise TypeError("Device not found! Check if you have provided the right name. Check also if you have opened the player.")


def _get_devices():
    """
    Return a list of available devices.
    """
    endpoint = "https://api.spotify.com/v1/me/player/devices"
    token = authenticate()
    headers = create_access_header(token)
    devices = requests.get(endpoint, headers=headers)
    if devices.status_code == 200:
        return devices.json()["devices"]
    else:
        message = json.loads(devices.text)["error"]["message"]
        raise ConnectionError(f"API status code {devices.status_code}: {message} ")


def get_current_album_cover():
    """Returns the id of the album that is currently played."""
    endpoint = "https://api.spotify.com/v1/me/player"
    access_token = authenticate()
    headers = create_access_header(access_token)
    playback_state = requests.get(endpoint, headers=headers)
    if playback_state.status_code == 200:
        state = playback_state.json()
        album_cover_url = state["item"]["album"]["images"][0]["url"]
        return album_cover_url

    else:
        message = json.loads(playback_state.text)["error"]["message"]
        raise ConnectionError(f"API status code {playback_state.status_code}: {message} ")
