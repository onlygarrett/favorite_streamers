from configparser import ConfigParser

def generate_twitch_user_config(parser: ConfigParser):
    
    user_access_token = input("Please input your access twitch access token for your account: ")
    client_id = input("Client ID for app needed, please input: ")
    user_id = input("Now please enter user ID: ")
    
    parser['config'] = {
        "accessToken": user_access_token,
        "clientId": client_id,
        "userId": user_id
    }
    
    with open("config.ini", 'w') as configuration:
        parser.write(configuration)