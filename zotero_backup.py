import shutil
import datetime
from pathlib import Path
import platform
import os


# Win10 DPI something
import ctypes
def make_dpi_aware() -> None:
    if int(platform.release()) >= 8:
        ctypes.windll.shcore.SetProcessDpiAwareness(True)
make_dpi_aware()


# SETTING. ONE AND ONLY
backup_dir = Path('G:\\Мой диск\\Zotero_backups')


# Zotero defaults
storage_dir = Path.home() / 'Zotero'
roaming = os.getenv('APPDATA')
profile_dir = Path(roaming) / 'Zotero'


# other things
now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
uname = platform.uname()
machine = f"{uname.system}_{uname.release}_{uname.node}"

storage_archive_name = f'{now}_storage_{machine}'
profile_archive_name = f'{now}_profile_{machine}'

backup_dir.mkdir(exist_ok=True)
storage_archive = backup_dir / storage_archive_name
profile_archive = backup_dir / profile_archive_name


# GUI
import PySimpleGUI as sg
sg.theme('DarkRed1')

layout = [
    [
        [sg.Text('Profile:', size=(8,1)), sg.Text(profile_dir)],
        [sg.Text('Storage:', size=(8,1)), sg.Text(storage_dir)],
    ],
    [
        sg.Frame(f'Backup: {backup_dir}\\', [
            [sg.Text(f'{storage_archive_name}.zip')],
            [sg.Text(f'{profile_archive_name}.zip')],
        ])
    ],
    [
        sg.Frame('Do it!', [[
            sg.Button('Backup!', key='backup', button_color=('white', 'green')),
        ]]),
        sg.Frame('Open', [[
            sg.Button('Profile dir', key='open_profile'),
            sg.Button('Storage dir', key='open_storage'),
            sg.Button('Backup dir', key='open_backup'),
        ]]),
    ]
]

window = sg.Window('Zotero Backup', layout, resizable=True, finalize=True)
while True:
    event, values = window.read()
    if event in (sg.WINDOW_CLOSED, "event_log_esc"):
        break

    if event == 'backup':
        # actual script - those 2 lines
        shutil.make_archive(storage_archive, format='zip', root_dir=storage_dir)
        shutil.make_archive(profile_archive, format='zip', root_dir=profile_dir)
        sg.Popup('Success', keep_on_top=True, auto_close = True, auto_close_duration = 1)

    if event == 'open_profile':
        os.startfile(profile_dir)

    if event == 'open_storage':
        os.startfile(storage_dir)

    if event == 'open_backup':
        os.startfile(backup_dir)

window.close()
