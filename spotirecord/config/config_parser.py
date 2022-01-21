"""Used to parse config data and client related data."""
import yaml
from pathlib import Path

basepath = Path(__file__).parent
config = basepath / "config.yml"
client = basepath / "client.yml"


def read_client_data():
    with open(client, "r") as file:
        return yaml.safe_load(file)


def read_config():
    with open(config, "r") as file:
        return yaml.safe_load(file)