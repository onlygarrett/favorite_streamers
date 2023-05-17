import asyncio, shlex
from pathlib import Path

"""
    command runner using asynchio
"""
async def run_command(command_script: str, dialog, result) -> None:
    '''Run a command in the background and display the output in the pre-created dialog.'''
    dialog.open()
    result.content = ''
    process = await asyncio.create_subprocess_exec(
        *shlex.split(command_script),
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
    
    if not result.content:
        result.content = 'Error when retrieving Streamer data, please confirm config is correct and try again.'