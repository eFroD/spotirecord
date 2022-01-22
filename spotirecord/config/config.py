"""Used to parse config data and client related data."""
import yaml
from pathlib import Path

basepath = Path(__file__).parent
config = basepath / "config.yml"
client = basepath / "client.yml"


def read_client_data():
    if client.exists():
        with open(client, "r") as file:
            return yaml.safe_load(file)
    else:
        return None


def read_config():
    with open(config, "r") as file:
        return yaml.safe_load(file)


def write_client_data(data):
    """
    Write the given dict to a yaml file as "client.yml"

    Args:
        data: a dict containing the fields that should be saved.
    """
    with open(client, "w") as out:
        yaml.dump(data, out, default_flow_style=False)
