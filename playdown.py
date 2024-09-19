from yt_dlp import YoutubeDL
from termcolor import colored, cprint
from tqdm import tqdm
from os import name
from subprocess import run
from tkinter import Tk, filedialog
from pathlib import Path
from time import sleep
from sys import exit
import shutil
import pkg_resources

def progress_hook(d):
    if d['status'] == 'finished':
        clear_screen()
        print('Done downloading, now converting ...')
    if d['status'] == 'downloading':
        pbar = tqdm(total=d['total_bytes'], unit='B', unit_scale=True, unit_divisor=1024)
        pbar.update(d['downloaded_bytes'])
        clear_screen()
    if d['status'] == 'error':
        clear_screen()
        print(colored('An error occurred while downloading the video.', 'red'))
        exit(1)

def download_video(url, path):
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': path + '/%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def convert_video(path):
    for file in Path(path).rglob('*.webm'):
        run(['ffmpeg', '-i', file, '-vn', '-ab', '128k', '-ar', '44100', '-y', str(file.with_suffix('.mp3'))])
    for file in Path(path).rglob('*.webm'):
        file.unlink()

def get_path():
    root = Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    return path

def clear_screen():
    if name == 'nt':
        _ = run('cls', shell=True)
    else:
        _ = run('clear', shell=True)

def print_banner():
    cprint('Playdown', 'green', attrs=['bold'])
    print('A simple tool to download and convert YouTube videos.')
    print()

def print_menu():
    print('1. Download and convert a video')
    print('2. Exit')
    print()

def download_and_convert():
    url = input('Enter the URL of the video: ')
    path = get_path()
    download_video(url, path)
    convert_video(path)
    print('The video has been downloaded and converted successfully.')

def check_requirements():
    # Check the requirements file requirements.txt
    with open('requirements.txt') as f:
        required = f.read().splitlines()
    installed = [pkg.key for pkg in pkg_resources.working_set]
    missing = [req for req in required if req not in installed]
    if missing:
        print('Installing the required packages ...')
        for package in missing:
            run(['pip', 'install', package])
        print('All required packages installed successfully.')
        sleep(2)
    else:
        print('All required packages are installed.')
        sleep(2)

    # Check if ffmpeg is installed
    if shutil.which('ffmpeg') is None:
        print('ffmpeg is not installed. Please install ffmpeg and add it to your PATH.')
        exit(1)
    else:
        print('ffmpeg is installed.')

def main():
    print_banner()
    check_requirements()

    while True:
        clear_screen()
        print_banner()
        print_menu()
        choice = input('Enter your choice: ')
        if choice == '1':
            download_and_convert()
            input('Press Enter to continue ...')
        elif choice == '2':
            exit()

if __name__ == '__main__':
    main()
