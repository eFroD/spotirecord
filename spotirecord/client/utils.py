"""Client related utilities"""
import base64
from urllib.parse import urlparse


def create_access_header(access_token):
    """
    Creates the headers for a get request
    """
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    return headers


def create_authorization_header(client_id, client_secret):
    """
    Creates the correctly encoded headers for access_token requests

    Args:
        client_id: the client id from the app
        client_secret: the corresponding client secret
    """
    client_data = client_id + ":" + client_secret
    header = {
        "Authorization": "Basic " + base64.urlsafe_b64encode(client_data.encode()).decode(),
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return header


def extract_uri(url):
    """
    Extracts the uri from the given url.

    Args:
        url: the url, that is also used for sharing tracks or albums.

    Returns:
        the uri to use it for the web api.
    """
    path = urlparse(url).path
    uri = "spotify"+":".join(path.split("/"))
    return uri
