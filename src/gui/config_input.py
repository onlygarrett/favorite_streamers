#!/usr/bin/env python3
from nicegui import ui
from ..backend import generate_twitch_user_config_from_input
from ..backend import ConfigInputError

from nicegui import ui

class ManualConfigInput(ui.dialog):
    
    def __init__(self) -> None:
        """
            Manual Config Input
            
            Dialog class handling the manual input of the config
        """
        
        super().__init__()
        self._access_token = None
        self._client_id = None
        self._user_id = None
        
        # bring up new card with inputs
        with self, ui.card():
            self._access_token = ui.input('Access Token').on('keydown.enter', self.confirm_config)
            self._client_id = ui.input('Client ID').on('keydown.enter', self.confirm_config)
            self._user_id = ui.input('User ID').on('keydown.enter', self.confirm_config)
            
            ui.button('Submit', on_click=self.confirm_config).props('color=secondary')
            
    # test dialog and then save
    def confirm_config(self):
        try:
            config_dict = dict(
                accessToken=self._access_token.value,
                clientId=self._client_id.value,
                userId=self._user_id.value
            )
            generate_twitch_user_config_from_input(config_dict)
            self.submit(True)
        except ConfigInputError as e:
            ui.notify(e)
        
async def input_config() -> None:
    result = await ManualConfigInput()
    if result:
        ui.notify(f'New config entered!')
    return