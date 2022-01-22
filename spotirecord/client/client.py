"""The client module manages the most important Spotify API related tasks."""
import requests
import json
import time

from spotirecord.config import read_config, write_client_data, read_client_data
from .authentication import authenticate

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
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/json"
    }
    devices = requests.get(endpoint, headers=headers)
    if devices.status_code == 200:
        return devices.json()["devices"]
    else:
        message = json.loads(devices.text)["error"]["message"]
        raise ConnectionError(f"API status code {devices.status_code}: {message} ")


