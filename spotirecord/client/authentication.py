"""This module is used if the user has no authentication settings yet."""
import sys
import yaml
import requests
import webbrowser
from urllib.parse import urlparse, parse_qs
from pathlib import Path

from spotirecord.config import read_client_data
from .utils import create_authorization_header

basepath = Path(__file__)
config_path = basepath.parents[1] / "config/client.yml"


def authenticate():
    """
    Checks if there is already a client configuration saved. If not, the
    authentication process will start.
    """

    if not config_path.exists():
        create_client()
    else:
        return get_access_token()


def create_client():
    """
    Initiates the whole creation procedure of a new client.

    Args:
        config_path: The location where the client data should be written.
    """
    scope = "user-read-playback-state user-modify-playback-state streaming"
    print("In order to use this program you need to register an app as a developer.")
    print("Visit https://developer.spotify.com/dashboard/login and log in your premium account.")
    print("Click on 'create an app' and follow the procedure")
    print("When done, click 'Edit Settings' and add the address http://localhost:8800 to your redirect URIs in the settings ")
    print("Come back, when you are ready.")
    client_id = input("Please enter the client id from your spotify dashboard: ")
    client_secret = input("Now enter the client secret: ")
    print("Thanks, follow the directions in the browser.\n"
          "After successfully logging in to spotify, ignore the page that opens up, just copy the link from your browser in here and press ENTER")
    webbrowser.open(f"https://accounts.spotify.com/authorize?client_id={client_id}&"
                    f"response_type=code&redirect_uri=http://localhost:8800&scope={scope}")
    auth_code_url = input("Paste the url from your browser: ")
    try:
        auth_code = parse_qs(urlparse(auth_code_url).query)["code"][0]
    except KeyError:
        print("Your url seems to have no code. Maybe the authorization did not work.\n"
              "Please start the program again.")
        sys.exit(1)

    params = {
        "code": auth_code,
        "redirect_uri": "http://localhost:8800",
        "grant_type": "authorization_code",
    }
    header = create_authorization_header(client_id, client_secret)
    access_response = requests.post("https://accounts.spotify.com/api/token", data=params, headers=header).json()
    refresh_token = access_response["refresh_token"]
    print(f"Successfully connected!\nYour data will be written at '{config_path}'.")
    with open(config_path, "w") as out:
        yaml.dump({"client_id": client_id,
                   "client_secret": client_secret,
                   "refresh_token": refresh_token}, out, default_flow_style=False)


def get_access_token():
    """
    Retrieves the access token from the user by using the refresh token in the config.
    """
    client_data = read_client_data()
    params = {
        "grant_type": "refresh_token",
        "refresh_token": client_data["refresh_token"]
    }
    headers = create_authorization_header(client_data["client_id"], client_data["client_secret"])
    result = requests.post('https://accounts.spotify.com/api/token', data=params, headers=headers).json()
    return result["access_token"]
