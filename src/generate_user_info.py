import sys, json, requests
from os.path import exists
from .config_gen import generate_twitch_user_config
from configparser import ConfigParser

def generate(parser: ConfigParser):
    if not exists('src/config.ini'):
        print("No config file detected.")
        generate_twitch_user_config(parser)
    else:
        parser.read('src/config.ini')
        parsed_config = parser['config']
        access_token = parsed_config['accessToken']
        client_id = parsed_config['clientId']
        
        regenerate_choice = input('Config file detected. Would you like to update the config? [no]: ') or 'no'
        if regenerate_choice.lower() == 'yes':
            generate_twitch_user_config(parser)

    parser.read('src/config.ini')

    parsed_config = parser['config']
    access_token = parsed_config['accessToken']
    client_id = parsed_config['clientId']
    user_id = parsed_config['userId']

    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + access_token
    }

    try:
        response = requests.get('https://api.twitch.tv/helix/streams/followed?user_id=' + user_id, headers=headers)
        
        data = response.json()['data']
        follow_count = len(data)
        
    except (KeyError, ValueError):
        print('Error with config values, please make sure they are correct.')
        sys.exit(1)
        
    certain_game = input('Do you want to display only specific games? If so enter the name of the game: ') or ""

        
    print ("\nCHANNEL " + ' '*13 + "GAME" + ' '*37 + "VIEWERS" + ' '*8 + "\n" + '-'*80)


    for i in range (0, follow_count):
        channel_name = data[i]["user_name"]
        channel_game = data[i]["game_name"]
        if certain_game and channel_game.lower() != certain_game.lower():
            continue
        
        channel_viewers = str(data[i]["viewer_count"])
        stream_type = data[i]["type"]

        if(stream_type == "live"):
            stream_type = ""
        else:
            stream_type = "(vodcast)"

        if(len(channel_name) > 18):
            channel_name = channel_name[:18] + ".."
        if(len(channel_game) > 38):
            channel_game = channel_game[:38] + ".."

        print ("{} {} {} {}".format(
        channel_name.ljust(20),
        channel_game.ljust(40),
        channel_viewers.ljust(8),
        stream_type
        ))

    if (i == follow_count-1):
        print ('-'*80)