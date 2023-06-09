import requests
from configparser import ConfigParser

"""
    This is basically a script that prints the data of the API endpoint
    but to be used with asynchio as a subprocess
"""

if __name__ == "__main__":
    parser = ConfigParser()

    # re-reading just in case of update
    parser.read('../backend/config.ini')

    parsed_config = parser['config']
    access_token = parsed_config['accessToken']
    client_id = parsed_config['clientId']
    user_id = parsed_config['userId']

    # request headers
    headers = {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': client_id,
        'Authorization': 'Bearer ' + access_token
    }

    # hitting API
    try:
        response = requests.get('https://api.twitch.tv/helix/streams/followed?user_id=' + user_id, headers=headers)
        
        data = response.json()['data']
        follow_count = len(data)
        # headers for print
        print ("\nCHANNEL " + ' '*13 + "GAME" + ' '*37 + "VIEWERS" + ' '*8 + "\n" + '-'*80)

        # bunch of prints w/ formatting
        for i in range (0, follow_count):
            channel_name = data[i]["user_name"]
            channel_game = data[i]["game_name"]
            # checking for specific game prompt
            
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
        
    except (KeyError, ValueError):
        pass