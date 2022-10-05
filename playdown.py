from pytube import YouTube, Playlist
from tkinter import filedialog, Tk as tk
import os

option_menu = {
    1: 'Baixar playlist',
    2: 'Baixar música',
    3: 'Sair'
}

def print_options():
    print()
    print("           ###                          ###                             ")
    print("            ##                           ##                             ")
    print(" ######     ##      ####    ##  ##       ##    ####    ##   ##  #####   ")
    print("  ##  ##    ##         ##   ##  ##    #####   ##  ##   ## # ##  ##  ##  ")
    print("  ##  ##    ##      #####   ##  ##   ##  ##   ##  ##   #######  ##  ##  ")
    print("  #####     ##     ##  ##    #####   ##  ##   ##  ##   #######  ##  ##  ")
    print("  ##       ####     #####       ##    ######   ####     ## ##   ##  ##  ")
    print(" ####                       #####                                       ")
    print()
    print()
    print('Bem-vindo ao PlayDown!')
    print('Escolha uma opção abaixo')
    print()
    for option in option_menu:
        print(f'{option}: {option_menu[option]}')

def get_option():
    print()
    option = int(input('Opção: '))
    return option

def main():
    print_options()
    option = get_option()
    if option == 1:
        limpar()
        download_playlist()
    elif option == 2:
        limpar()
        download_music()
    elif option == 3:
        print('Saindo...')
        os.system('exit' if os.name == 'nt' else 'exit')
    else:
        print('Número inválido!')

def format_title(title):
    new_title = ''
    for ch in title:
        if ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_()[]{} ':
            new_title += ch
    return new_title

def download_playlist():
    print('--------------------------------------------------------')
    print('Insira o URL da playlist que deseja baixar')
    print('Exemplo: https://www.youtube.com/playlist?list=XXXXXXXXXXX')
    print('--------------------------------------------------------')
    link = input('Link: ')
    playlist = Playlist(link)
    acre = 0
    print('Escolha o local para salvar a playlist')
    root = tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    print()
    for url in playlist:
        music = YouTube(url)
        name = format_title(music.title)
        author = format_title(music.author)

        # Baixar música e criar pasta com o nome do artista
        music.streams.get_audio_only().download(f'{file_path}/{author}', filename=f'{name}' + '.mp3', skip_existing=True)
        acre += 1

        print(f'Baixado com sucesso! {name} - {author} \n')

    if input('Deseja baixar outra playlist? (s/n) ') == 's':
        limpar()
        download_playlist()
    else:
        limpar()
        main()


def salvar(audio):
    audio.save()


def download_music():
    print()
    print('Insira o URL da musica que deseja baixar')
    print('Exemplo: https://www.youtube.com/watch?v=XXXXXXXXXXX')
    print()
    link = input('Link: ')
    music = YouTube(link)
    name = format_title(music.title)
    print('Escolha o local para salvar a musica')
    root = tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    author = format_title(music.author)
    print()

    # Baixar música e criar pasta com o nome do artista
    print(f'Baixando {name} - {author}...')
    music.streams.get_audio_only().download(f'{file_path}/{author}', filename=f'{name}' + '.mp3', skip_existing=True)
    print(f'Baixado com sucesso! {name} - {author} \n')

    if input('Deseja baixar outra musica? (s/n) ') == 's':
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
