from email.mime import audio
import os
from tkinter import Tk as tk
from tkinter import filedialog
from termcolor import colored, cprint
from time import sleep
from tqdm import tqdm

from pytube import Playlist
from pytube import YouTube

option_menu = {1: "Baixar playlist", 2: "Baixar música", 3: "Sair"}

# Titulo do programa
titulo = "PlayDown"
os.system("title " + titulo if os.name == "nt" else "PS1='\[\e]0;" + titulo + "\a\]'; echo $PS1")

# tamanho do cmd para windows e linux
if os.name == 'nt':
    os.system('mode con: cols=100 lines=25')
else:
    os.system('resize -s 30 100')

def print_options():
    print()
    cprint('                           _____  _             _____                      ', 'magenta', attrs=['bold'])   
    cprint('                          |  __ \| |           |  __ \                     ', 'magenta', attrs=['bold'])
    cprint('                          | |__) | | __ _ _   _| |  | | _____      ___ __  ', 'magenta', attrs=['bold'])
    cprint('                          |  ___/| |/ _` | | | | |  | |/ _ \ \ /\ / /  _ \ ', 'magenta', attrs=['bold'])
    cprint('                          | |    | | (_| | |_| | |__| | (_) \ V  V /| | | |', 'magenta', attrs=['bold'])
    cprint('                          |_|    |_|\__,_|\__, |_____/ \___/ \_/\_/ |_| |_|', 'magenta', attrs=['bold'])
    cprint('                                           __/ |                           ', 'magenta', attrs=['bold'])
    cprint('                                          |___/                            ', 'magenta', attrs=['bold'])
    print()
    cprint(' ------------------------------ Bem-Vindo, escolha uma opção abaixo. ------------------------------ ', 'white', attrs=['bold'])
    print()
    for option in option_menu:
        cprint(f'  | {option}: {option_menu[option]}', 'white', attrs=['bold'])


def get_option():
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    option = input(f'  | {symbol_more_than} opção: ')
    return option


def main():
    print_options()
    option = get_option()
    if option == '1':
        limpar()
        download_playlist()
    elif option == '2':
        limpar()
        download_music()
    elif option == '3':
        limpar()
        exit()
    else:
        cprint('Opção inválida!', 'red', attrs=['bold'])
        main()


def format_title(title):
    new_title = ''
    for ch in title:
        if (
            ch
            not in 'áàãâéêíóôõúüçÁÀÃÂÉÊÍÓÔÕÚÜÇ!@#$%¨&*()_+{}[]:;?/.,><`¬^~´°ºª|'
        ):
            new_title += ch
    return new_title


def download_playlist():
    print()
    cprint(' Insira o URL da playlist que deseja baixar', 'white', attrs=['bold'])
    cprint(' Exemplo: https://www.youtube.com/playlist?list=XXXXXXXXXXX', 'white', attrs=['bold'])
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    link = input(f'  | {symbol_more_than} Link: ')
    playlist = Playlist(link)
    acre = 0
    cprint(' Escolha o local para salvar a playlist', 'white', attrs=['bold'])
    root = tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    print()
    for url in playlist:
        music = YouTube(url)
        name = format_title(music.title)
        playlist_name = format_title(playlist.title)

        # progress bar tqdm
        for i in tqdm(range(100), desc=f' Baixando {name}'):
            sleep(0.01)
        # Baixar música e criar pasta com o nome do artista
        music.streams.get_audio_only().download(
            f'{file_path}/{playlist_name}', filename=f'{name}' + '.mp3', skip_existing=True
        )
        acre += 1
        cprint(f' {acre} de {len(playlist)}', 'white', attrs=['bold'])
    cprint(' Playlist baixada com sucesso!', 'green', attrs=['bold'])
    if input(' Deseja baixar outra playlist? [S/N] ').lower() == 's':
        limpar()
        download_playlist()
    else:
        limpar()
        main()


def salvar(audio):
    audio.save()


def download_music():
    print()
    cprint('  Insira o URL da musica que deseja baixar', 'white', attrs=['bold'])
    cprint('  Exemplo: https://www.youtube.com/watch?v=XXXXXXXXXXX', 'white', attrs=['bold'])
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    link = input(f' | {symbol_more_than} Link: ')
    music = YouTube(link)
    name = format_title(music.title)
    print('Escolha o local para salvar a musica')
    root = tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    music_name = format_title(music.title)
    print()

    # progress bar tqdm
    for i in tqdm(range(100), desc=f' Baixando {music_name}'):
        sleep(0.01)
    # Baixar música e criar pasta com o nome do artista
    music.streams.get_audio_only().download(
        f'{file_path}' + '/Musics PlayDown', filename=f'{music_name}' + '.mp3', skip_existing=True
    )
    cprint(f' {name} baixada com sucesso!', 'white', attrs=['bold'])

    if input(" Deseja baixar outra musica? (s/n) ") == "s":
        limpar()
        download_music()
    else:
        limpar()
        main()


def limpar():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')


if __name__ == '__main__':
    main()
