from configparser import ConfigParser
from pathlib import Path
from .error_handling import ConfigImportError, ConfigInputError

"""
    config saving functions.
    one to save from file and the other from a dict
"""
def generate_twitch_user_config_from_file(new_config_location: str):
    parser = ConfigParser()
    
    # re-reading just in case of update
    file_location = Path(new_config_location)
    parser.read(file_location)
    
    if not parser.has_section('config') or \
        not parser.has_option('config', 'accessToken') or not parser.has_option('config', 'clientId') or \
            not parser.has_option('config', 'userId'):
        raise ConfigImportError
                
    with open("src/backend/config.ini", 'w') as configuration:
        parser.write(configuration)
        
def generate_twitch_user_config_from_input(config_input: dict):
    if not all(config_input.values()):
        raise ConfigInputError
    else:
        parser = ConfigParser()
        parser.add_section('config')
        parser.set('config', 'accessToken', str(config_input['accessToken']))
        parser.set('config', 'clientId', str(config_input['clientId']))
        parser.set('config', 'userId', str(config_input['userId']))
                    
        with open("src/backend/config.ini", 'w') as configuration:
            parser.write(configuration)