# Programa feito pelo ObvTago <3

from pytube import YouTube
from pytube import Playlist

import os

link = input("Insira o link de uma playlist: ")
yt = Playlist(link)  # pega 0 link da playlist enviada pelo usúario
acre = 0;
for url in yt.video_urls:
    ys = YouTube(url)
    print(ys.title)
    vid = ys.streams.get_audio_only()
    out_file = vid.download()
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    print("Concluído")

print("Downloads concluidos!")
print("By ObvTago :D")
