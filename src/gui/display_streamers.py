import sys, requests
from nicegui import ui
from configparser import ConfigParser
from ..backend import command_runner
from pathlib import Path
from ..backend.error_handling import ApiError

TWITCH_FOLLOWER_URL = 'https://api.twitch.tv/helix/streams/followed?user_id='

class DisplayStreamerButton(ui.dialog):

    def __init__(self):
        """Display Streamer Button
        
        Button Class with dialog for rendering output of streamers
        
        """
        super().__init__()
        # access info
        self._access_token = None
        self._client_id = None
        self._user_id = None
        # request headers
        self.headers = None
        # response info
        self.data = None
        self.follow_count = None
        # output
        self.output = None
        # actual work
        self.grab_ini_file()
        self.send_request()
        self.print_data()
        
    # grabbing saved .ini file in repo
    def grab_ini_file(self):
        parser = ConfigParser()

        # re-reading just in case of update
        file_location = Path(command_runner.__file__).parent / 'config.ini'
        parser.read(file_location)

        parsed_config = parser['config']
        self._access_token = parsed_config['accessToken']
        self._client_id = parsed_config['clientId']
        self._user_id = parsed_config['userId']
        
        # required headers for twitch API
        self.headers = {
            'Accept': 'application/vnd.twitchtv.v5+json',
            'Client-ID': self._client_id,
            'Authorization': 'Bearer ' + self._access_token
        }
        
    # function for hitting endpoint
    def send_request(self):
        # hitting API
        try:
            response = requests.get(TWITCH_FOLLOWER_URL + self._user_id, headers=self.headers)
            
            self.data = response.json()['data']
            self.follow_count = len(self.data)
            
        except (KeyError, ValueError): # basically if no data on response
            raise ApiError

    # printing using nicegui's table element
    def print_data(self):
        columns = [
            {'name': 'channel', 'label': 'Channel', 'field': 'channel', 'required': True, 'align': 'left'},
            {'name': 'game', 'label': 'Game', 'field': 'game'},
            {'name': 'viewers', 'label': 'Viewers', 'field': 'viewers', 'sortable': True}
        ]
        rows = []

        # bunch of prints w/ formatting
        for i in range (0, self.follow_count):
            channel_name = self.data[i]["user_name"]
            channel_game = self.data[i]["game_name"]
            # checking for specific game prompt
            # TODO
            
            channel_viewers = self.data[i]["viewer_count"]
            new_entry = dict(
                channel=channel_name,
                game=channel_game,
                viewers=channel_viewers
            )
            rows.append(new_entry)
        with self, ui.card():
            ui.table(columns=columns, rows=rows, row_key='channel')
            
async def streamers() -> None:
    try:
        result = await DisplayStreamerButton()
    except ApiError as e:
        ui.notify(e)
        return