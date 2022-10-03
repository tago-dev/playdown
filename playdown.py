from pytube import YouTube, Playlist
from os import system as cmd
import os
import random
import tkinter as tk
from tkinter import filedialog
import time

option_menu = {
    1: "Baixar playlist (music)",
    2: "Baixar musica",
    3: "Sair",
}

def print_options():
    print("------------------------------------------------------------------------")
    print("          ###                          ###                              ")
    print("           ##                           ##                              ")
    print(" ######     ##      ####    ##  ##       ##    ####    ##   ##  #####   ")
    print("  ##  ##    ##         ##   ##  ##    #####   ##  ##   ## # ##  ##  ##  ")
    print("  ##  ##    ##      #####   ##  ##   ##  ##   ##  ##   #######  ##  ##  ")
    print("  #####     ##     ##  ##    #####   ##  ##   ##  ##   #######  ##  ##  ")
    print("  ##       ####     #####       ##    ######   ####     ## ##   ##  ##  ")
    print(" ####                       #####                                       ")
    print("------------------------------------------------------------------------")
    print("Welcome to Playdown!")
    print("Escolha uma opção abaixo")
    print("------------------------------------------------------------------------")
    for option in option_menu:
        print(f"{option} - {option_menu[option]}")

def get_option():
    print("------------------------------------------------------------------------")
    option = int(input(">>> "))
    return option

def main():
    print_options()
    option = get_option()
    if option == 1:
        os.system("cls" if os.name == "nt" else "clear")
        download_playlist()
    elif option == 2:
        os.system("cls" if os.name == "nt" else "clear")
        download_music()
    elif option == 3:
        print("Saindo...")
        exit()

def format_title(title):
    new_title = ''
    for ch in title:
        if ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_()[]{} ':
            new_title += ch
    return new_title

def download_playlist():
    print("--------------------------------------------------------")
    print("Insira o URL da playlist que deseja baixar")
    print("Exemplo: https://www.youtube.com/playlist?list=XXXXXXXXXXX")
    print(time.strftime("%d/%m/%Y"))
    print("--------------------------------------------------------")
    link = input(">>> ")
    playlist = Playlist(link)
    acre = 0
    x = random.randint(1, 100000)
    print("escolha o local para salvar a playlist")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    for url in playlist:
        music = YouTube(url)
        name = format_title(music.title)
        music.streams.get_audio_only().download(f"{file_path}", filename=f"{name}" + ".mp3")
        acre += 1
        print(f"Baixado {acre} de {len(playlist)}")
    print("Baixado com sucesso! \n")

    if input("Deseja baixar outra playlist? (s/n) ") == "s":
        os.system("cls" if os.name == "nt" else "clear")
        download_playlist()
    else:
        main()


def download_music():
    print("--------------------------------------------------------")
    print("Insira o URL da musica que deseja baixar")
    print("Exemplo: https://www.youtube.com/watch?v=XXXXXXXXXXX")
    print(time.strftime("%d/%m/%Y"))
    print("--------------------------------------------------------")
    link = input(">>> ")
    music = YouTube(link)
    name = format_title(music.title)
    print("escolha o local para salvar a musica")
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    music.streams.get_audio_only().download(f"{file_path}", filename=f"{name}" + ".mp3")
    print("Baixado com sucesso! \n")

    if input("Deseja baixar outra musica? (s/n) ") == "s":
        os.system("cls" if os.name == "nt" else "clear")
        download_music()
    else:
        main()

if __name__ == '__main__':
    main()