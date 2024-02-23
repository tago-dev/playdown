from os import system as cmd, name as os_name
from pathlib import Path
from sys import exit
from time import sleep
from tkinter import Tk, filedialog
from pytube import YouTube, Playlist
from termcolor import colored, cprint
from tqdm import tqdm


option_menu = {1: 'Download playlist', 2: 'Download music', 3: 'Exit'}

# Program Title
title = 'PlayDown'
cmd('title ' + title if os_name == 'nt' else r"PS1='\[\e]0;" + title + r"\a\]'; echo $PS1")

# CMD size for Windows and Linux
if os_name == 'nt':
    cmd('mode con: cols=100 lines=25 >nul 2>&1')
else:
    cmd('resize -s 30 100')


<<<<<<< Updated upstream
def print_options():
    print()
    cprint('                           _____  _             _____                      ', 'magenta', attrs=['bold'])
    cprint('                          |  __ \| |           |  __ \                     ', 'magenta', attrs=['bold'])
    cprint('                          | |__) | | __ _ _   _| |  | | _____      ___ __  ', 'magenta', attrs=['bold'])
    cprint('                          |  ___/| |/ _` | | | | |  | |/ _ \ \ /\ / /  _ \ ', 'magenta', attrs=['bold'])
    cprint('                          | |    | | (_| | |_| | |__| | (_) \ V  V /| | | |', 'magenta', attrs=['bold'])
    cprint('                          |_|    |_|\__,_|\__, |_____/ \___/ \_/\_/ |_| |_|', 'magenta', attrs=['bold'])
    cprint('                                           __/ | Criado por: @tago.dev     ', 'magenta', attrs=['bold'])
    cprint('                                          |___/ gh: github.com/tago-dev    ', 'magenta', attrs=['bold'])
    print()
    cprint(' ------------------------------ Bem-Vindo, escolha uma opção abaixo. ------------------------------ ', 'white', attrs=['bold'])
    print()
=======
def clear() -> None:
    if os_name == 'nt':
        cmd('cls >nul 2>&1')
    else:
        cmd('clear')


def print_options() -> None:
    cprint('\n                           _____  _             _____                      ', 'magenta', attrs=['bold'])
    cprint(r'                          |  __ \| |           |  __ \                     ', 'magenta', attrs=['bold'])
    cprint(r'                          | |__) | | __ _ _   _| |  | | _____      ___ __  ', 'magenta', attrs=['bold'])
    cprint(r'                          |  ___/| |/ _` | | | | |  | |/ _ \ \ /\ / /  _ \ ', 'magenta', attrs=['bold'])
    cprint(r'                          | |    | | (_| | |_| | |__| | (_) \ V  V /| | | |', 'magenta', attrs=['bold'])
    cprint(r'                          |_|    |_|\__,_|\__, |_____/ \___/ \_/\_/ |_| |_|', 'magenta', attrs=['bold'])
    cprint(r'                                           __/ | Created by: @tago.dev     ', 'magenta', attrs=['bold'])
    cprint('                                          |___/ gh: github.com/tago-dev    ', 'magenta', attrs=['bold'])
    cprint('\n ------------------------------ Welcome, choose an option below. ------------------------------ \n', 'white', attrs=['bold'])
>>>>>>> Stashed changes

    for option in option_menu:
        cprint(f' | {option}: {option_menu[option]}', 'white', attrs=['bold'])


def get_option() -> str:
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    option = input(f'\n | {symbol_more_than} Option: ')
    return option


def main() -> None:
    print_options()
    option = get_option()
    if option == '1':
        clear()
        download_playlist()
    elif option == '2':
        clear()
        download_music()
    elif option == '3':
        clear()
        app_exit()
    else:
        cprint('Invalid option!', 'red', attrs=['bold'])
        main()


def format_title(title_name: str) -> str:
    return str().join(['-' if char == '/' else char for char in title_name])


def download_playlist() -> None:
    print()
    cprint('   Insert the playlist URL you want to download', 'white', attrs=['bold'])
    cprint('   Example: https://www.youtube.com/playlist?list=XXXXXXXXXXX', 'white', attrs=['bold'])
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    link = input(f'  | {symbol_more_than} Link: ')
    playlist = Playlist(link)
    count = 0

    cprint('   Choose the location to save the playlist', 'white', attrs=['bold'])
    root = Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(title='Choose the location to save the music/playlist', initialdir=Path.cwd())
    print()

    for url in playlist:
        music = YouTube(url)
        name = format_title(music.title)
        playlist_name = format_title(playlist.title)

        # TQDM progress bar
        for _ in tqdm(range(100), desc=f' Downloading {name}'):
            sleep(0.01)

        # Download music and save in the folder
        music.streams.filter(only_audio=True).first().download(file_path + '/' + playlist_name, filename=name + '.mp3')
        count += 1
        cprint(f' {count} of {len(playlist)}', 'white', attrs=['bold'])

    cprint(' | Playlist downloaded successfully!', 'green', attrs=['bold'])
    if input(' | Do you want to download another playlist? [Y/N] ').lower() == 'y':
        clear()
        download_playlist()
    else:
        clear()
        main()


def download_music() -> None:
    print()
    cprint('  Insert the music URL you want to download', 'white', attrs=['bold'])
    cprint('  Example: https://www.youtube.com/watch?v=XXXXXXXXXXX', 'white', attrs=['bold'])
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    link = input(f' | {symbol_more_than} Link: ')
    music = YouTube(link)
    name = format_title(music.title)
    print('  Choose the location to save the music')
    root = Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(initialdir=Path.cwd())
    print()

    # TQDM progress bar
    for _ in tqdm(range(100), desc=f' Downloading {name} '):
        sleep(0.01)

    # Download music with artist and music name
    music.streams.get_audio_only().download(f'{file_path}', filename=f'{name}' + '.mp3')
    cprint(f' | {name} downloaded successfully!', 'white', attrs=['bold'])

    if input(' | Do you want to download another music? (y/n) ') == 'y':
        clear()
        download_music()
    else:
        clear()
        main()


def app_exit() -> None:
    clear()
    cprint('\n | Thank you for using PlayDown!', 'white', attrs=['bold'])
    cprint(' | Developed by: @tago.dev', 'white', attrs=['bold'])
    sleep(2)
    exit()


if __name__ == '__main__':
    main()
