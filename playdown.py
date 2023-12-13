from os import system as cmd, name as os_name
from pathlib import Path
from sys import exit
from time import sleep
from tkinter import Tk, filedialog
from pytube import YouTube, Playlist
from termcolor import colored, cprint
from tqdm import tqdm


option_menu = {1: 'Baixar playlist', 2: 'Baixar música', 3: 'Sair'}

# Título do programa
titulo = 'PlayDown'
cmd('title ' + titulo if os_name == 'nt' else "PS1='\[\e]0;" + titulo + "\a\]'; echo $PS1")

# Tamanho do CMD para Windows e Linux
if os_name == 'nt':
    cmd('mode con: cols=100 lines=25')
else:
    cmd('resize -s 30 100')


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
        app_exit()
    else:
        cprint('Opção inválida!', 'red', attrs=['bold'])
        main()


def format_title(title):
    new_title = str()
    for char in title:
        if char == '/':
            new_title += '-'
        else:
            new_title += char

    return new_title


def download_playlist():
    print()
    cprint('   Insira o URL da playlist que deseja baixar', 'white', attrs=['bold'])
    cprint('   Exemplo: https://www.youtube.com/playlist?list=XXXXXXXXXXX', 'white', attrs=['bold'])
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    link = input(f'  | {symbol_more_than} Link: ')
    playlist = Playlist(link)
    acre = 0

    cprint('   Escolha o local para salvar a playlist', 'white', attrs=['bold'])
    root = Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(initialdir=Path.cwd())
    print()

    for url in playlist:
        music = YouTube(url)
        name = format_title(music.title)
        playlist_name = format_title(playlist.title)

        # Barra de progresso TQDM
        for i in tqdm(range(100), desc=f' Baixando {name}'):
            sleep(0.01)

        # Baixar música e salvar na pasta
        music.streams.filter(only_audio=True).first().download(file_path + '/' + playlist_name, filename=name + '.mp3')
        acre += 1
        cprint(f' {acre} de {len(playlist)}', 'white', attrs=['bold'])

    cprint(' | Playlist baixada com sucesso!', 'green', attrs=['bold'])
    if input(' | Deseja baixar outra playlist? [S/N] ').lower() == 's':
        limpar()
        download_playlist()
    else:
        limpar()
        main()


def download_music():
    print()
    cprint('  Insira o URL da musica que deseja baixar', 'white', attrs=['bold'])
    cprint('  Exemplo: https://www.youtube.com/watch?v=XXXXXXXXXXX', 'white', attrs=['bold'])
    print()
    symbol_more_than = colored('>', 'magenta', attrs=['bold'])
    link = input(f' | {symbol_more_than} Link: ')
    music = YouTube(link)
    name = format_title(music.title)
    print('  Escolha o local para salvar a musica')
    root = Tk()
    root.withdraw()
    file_path = filedialog.askdirectory(initialdir=Path.cwd())
    print()

    # Barra de progresso TQDM
    for i in tqdm(range(100), desc=f' Baixando {name} '):
        sleep(0.01)

    # Baixar música com o nome do artista e da música
    music.streams.get_audio_only().download(f'{file_path}', filename=f'{name}' + '.mp3')
    cprint(f' | {name} baixada com sucesso!', 'white', attrs=['bold'])

    if input(' | Deseja baixar outra musica? (s/n) ') == 's':
        limpar()
        download_music()
    else:
        limpar()
        main()


def limpar():
    if os_name == 'nt':
        cmd('cls')
    else:
        cmd('clear')


def app_exit():
    limpar()
    cprint(' | Obrigado por utilizar o PlayDown!', 'white', attrs=['bold'])
    cprint(' | Desenvolvido por: tago', 'white', attrs=['bold'])
    sleep(2)
    exit()


if __name__ == '__main__':
    main()
