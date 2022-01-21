"""The client module manages the most important Spotify API related tasks."""
import requests
import json

from spotirecord.config import read_config
from .authentication import authenticate

conf = read_config()


def get_device_id():
    device_name = conf["device_name"]
    devices = _get_devices()
    device = next((item for item in devices if item["name"] == device_name), None)
    if device:
        return device["id"]
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


