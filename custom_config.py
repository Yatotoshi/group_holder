import configparser
import os

THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))


def config_load(section, key):
    config = configparser.ConfigParser()
    config.read(os.path.join(THIS_FOLDER, "config.ini"))
    return config[section][key]
