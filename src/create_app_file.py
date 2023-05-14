import os, subprocess
import nicegui, configparser
from pathlib import Path
from src.gui import file_upload
from backend import simple_output

cmd = [
    'python',
    '-m', 'PyInstaller',
    'src/gui/gui_generation.py', # your main file with ui.run()
    '--name', 'streamer_app', # name of your app
    '--clean', # clean up that big file
    '--onefile',
    '--distpath', f'{Path.cwd() / "bin"}',
    '--specpath', f'{Path.cwd()}',
    '--noconfirm',
    '--windowed', # prevent console appearing, only use with ui.run(native=True, ...)
    '--add-data', f'{Path(nicegui.__file__).parent}{os.pathsep}nicegui', # making paths for necessary calls
    '--add-data', f'{Path(configparser.__file__).parent}{os.pathsep}configparser',
    '--add-data', f'{Path(file_upload.__file__).parent}{os.pathsep}./src/gui',
    '--add-data', f'{Path(simple_output.__file__).parent}{os.pathsep}./src/backend'
]
subprocess.call(cmd)