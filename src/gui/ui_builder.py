#!/usr/bin/env python
import platform
from nicegui import background_tasks, ui
from src.gui.file_uploader import pick_file
from src.gui import streamers, input_config
from src.backend import run_command, STREAMER_SCRIPT

text_body = \
"""# Favorite Streamers App

This is a simple Python GUI application that uses Twitch.tv's helix API to grab current viewership 
of the streamers that a given user follows.

---

To hit this endpoint this certain endpoint Twitch requires 3 variables that associates the request with a given user:

 - A **Client Id** and an **Authorization token**
	 - Both of these can be retrieved from the link below with the `user:read:follows` scope.
 - A **User Id** 
	 - which can be grabbed from another handy generator link below

These variables can be entered through a manual input or by a `config.ini` file that the user can save to the app.

---

#### The reason for two buttons to output viewership was just to mess around with executing a script from an application. 
##### I have no further plan's to update this at the moment it was just to try out creating a simple GUI with Python.
You are more than welcome to branch off make your own tweaks!


"""
    

class UiBuilder():
    
    def __init__(self):
        """UI Builder

        Small class to create the whole UI of the app.
        
        """
        
        # text body
        with ui.row():
            ui.markdown(text_body).style(replace='color: white;')
            ui.link(text='Authorization Token and Client Id', target='https://twitchtokengenerator.com/',
                new_tab=True).classes('text-2xl')
            ui.link(text='User Id', target='https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/',
                new_tab=True).classes('text-2xl')
            
        # footer with buttons
        with ui.footer().style(replace='display: grid;') as footer:
            self.command_button(script_location=STREAMER_SCRIPT)
            self.display_streamer_button()
            self.config_button()
    
    # setting colors for app
    def change_colors(self, background: str, primary: str, secondary: str):
        ui.query('body').style(f'background-color: {background}')
        
        ui.query('footer').style(f'background-color: {primary}')
        ui.colors(primary=primary)
        ui.colors(secondary=secondary)
             
    # function to create config option select
    def config_button(self):
        ui.button('Change Config...', on_click=self.new_config_options
                    ).props('icon=cached').props('color=secondary')
        
    # rendering config button selection
    async def new_config_options(self):
        with ui.dialog() as config_dialog, ui.card():
            
            ui.label('How would you like to change the config?')
            with ui.row():
                self.file_upload_button() # file upload
                self.config_input_button() # manual input
                ui.button('Close', on_click=config_dialog.close).props('color=secondary')
    
        config_dialog.open()
        
    # file upload button render
    def file_upload_button(self):
        ui.button('Choose file', on_click=pick_file).props('icon=folder').props('color=secondary')
        
    # manual input button render
    def config_input_button(self):
        ui.button('Input manually', on_click=input_config).props('icon=input').props('color=secondary')
    
    # button for regular display
    def display_streamer_button(self):
        ui.button('Display Streamers with Python', on_click=streamers).props('icon=analytics').props('color=secondary')
        
    # similar button but this runs a background task with asynchio
    def command_button(self, script_location: str):
        with ui.dialog() as command_dialog, ui.card():
            result = ui.markdown()
        
        ui.button(
            'Display Streamers with Command script',
            on_click=lambda _,
            c=script_location: background_tasks.create(
                run_command(c, dialog=command_dialog, result=result))
            ).props('icon=analytics').props('color=secondary')
        
    # create gui
    def start_gui(self):
        self.change_colors(background="#2f373f", primary='#677da0', secondary='#561467')
        ui.run(
                title='Twitch Streamer Metrics',
                native=True, # for non-browser
                window_size=(1200, 1000),
                reload=platform.system() != "Windows" # nicegui is weird
            )

if __name__ == "__main__":
    pass