#!/usr/bin/env python3
from nicegui import ui
from pathlib import Path
from typing import Dict, Optional
from src.backend.config_gen import generate_twitch_user_config_from_file
from src.backend import ConfigImportError

from nicegui import ui

# most of this was from nicegui

class LocalFilePicker(ui.dialog):
    
    def __init__(self, directory: str, *,
                 upper_limit: Optional[str] = ..., multiple: bool = False, show_hidden_files: bool = False) -> None:
        """Local File Picker

        This is a simple file picker that allows you to select a file from the local filesystem where NiceGUI is running.

        :param directory: The directory to start in.
        :param upper_limit: The directory to stop at (None: no limit, default: same as the starting directory).
        :param multiple: Whether to allow multiple files to be selected.
        :param show_hidden_files: Whether to show hidden files.
        """
        super().__init__()

        self.path = Path(directory).expanduser()
        if upper_limit is None:
            self.upper_limit = None
        else:
            self.upper_limit = Path(directory if upper_limit == ... else upper_limit).expanduser()
        self.show_hidden_files = show_hidden_files

        with self, ui.card():
            self.grid = ui.aggrid({
                'columnDefs': [{'field': 'name', 'headerName': 'File'}],
                'rowSelection': 'multiple' if multiple else 'single',
            }, html_columns=[0]).classes('w-96').on('cellDoubleClicked', self.handle_double_click)
            with ui.row().classes('w-full justify-end'):
                ui.button('Cancel', on_click=self.close).props('outline')
                ui.button('Ok', on_click=self._handle_ok)
        self.update_grid()

    def update_grid(self) -> None:
        paths = list(self.path.glob('*'))
        if not self.show_hidden_files:
            paths = [p for p in paths if not p.name.startswith('.')]
        paths.sort(key=lambda p: p.name.lower())
        paths.sort(key=lambda p: not p.is_dir())

        self.grid.options['rowData'] = [
            {
                'name': f'📁 <strong>{p.name}</strong>' if p.is_dir() else p.name,
                'path': str(p),
            }
            for p in paths
        ]
        if self.upper_limit is None and self.path != self.path.parent or \
                self.upper_limit is not None and self.path != self.upper_limit:
            self.grid.options['rowData'].insert(0, {
                'name': '📁 <strong>..</strong>',
                'path': str(self.path.parent),
            })
        self.grid.update()
      
    # added this to handle the actual saving of file because nicegui doesn't
    def handle_upload(self, file: str):
        generate_twitch_user_config_from_file(file)
            

    async def handle_double_click(self, msg: Dict) -> None:
        self.path = Path(msg['args']['data']['path'])
        if self.path.is_dir():
            self.update_grid()
        else:
            try:
                self.handle_upload(self.path)
            except ConfigImportError as e: # my error handling
                ui.notify(e)
                return
            self.submit([str(self.path)])

    async def _handle_ok(self):
        rows = await ui.run_javascript(f'getElement({self.grid.id}).gridOptions.api.getSelectedRows()')
        try:
            self.handle_upload(rows[0]['path'])
        except ConfigImportError as e: # my error handling
            ui.notify(e)
            return
        self.submit(str(rows[0]['path']))


async def pick_file() -> None:
    result = await LocalFilePicker(f'{Path.cwd()}', multiple=True, upper_limit=None)
    ui.notify(f'You chose {result}')
    return
