#!/usr/bin/env python
import asyncio, shlex, platform
from pathlib import Path
from nicegui import background_tasks, ui

from .file_upload import pick_file

async def run_command(command: str) -> None:
    '''Run a command in the background and display the output in the pre-created dialog.'''
    dialog.open()
    result.content = ''
    process = await asyncio.create_subprocess_exec(
        *shlex.split(command),
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT,
        cwd=f'{Path(__file__).parent}'
    )
    # NOTE we need to read the output in chunks, otherwise the process will block
    output = ''
    while True:
        new = await process.stdout.read(4096)
        if not new:
            break
        output += new.decode()
        # NOTE the content of the markdown element is replaced every time we have new output
        result.content = f'```\n{output}\n```'

with ui.dialog() as dialog, ui.card():
    result = ui.markdown()

commands = ['python ../backend/simple_output.py', 'python file_upload.py']
display_streamer_script = 'python ../backend/simple_output.py'
with ui.row():
    ui.button(display_streamer_script, on_click=lambda _, c=display_streamer_script: background_tasks.create(run_command(c))).props('no-caps')
    ui.button('Choose file', on_click=pick_file).props('icon=folder')

ui.query('body').style(f'background-color: {"#2f373f"}')
# NOTE on windows reload must be disabled to make asyncio.create_subprocess_exec work (see https://github.com/zauberzeug/nicegui/issues/486)
ui.run(title='Twitch Streamer Metrics', native=True, window_size=(800, 800), reload=platform.system() != "Windows")