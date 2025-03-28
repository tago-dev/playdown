import os
import sys
import yt_dlp

def progress_hook(d):
    if d['status'] == 'downloading':
        if 'total_bytes' in d and d['total_bytes'] > 0:
            progress = d['downloaded_bytes'] / d['total_bytes']
            print(f"Download progress: {progress:.1%}")
        elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
            progress = d['downloaded_bytes'] / d['total_bytes_estimate']
            print(f"Download progress (estimate): {progress:.1%}")
    elif d['status'] == 'finished':
        print("Download finished!")
    elif d['status'] == 'error':
        print(f"Error occurred: {d.get('error')}")

def download_mp4(url, output_dir=None):
    """Download a YouTube video in MP4 format without requiring FFmpeg"""
    
    if not output_dir:
        output_dir = os.path.join(os.path.expanduser("~"), "Downloads")
    
    print(f"Downloading video from {url} to {output_dir}")
    
    # Set options for MP4 download (no merging needed to avoid FFmpeg requirement)
    ydl_opts = {
        # This format spec avoids merging and prefers a single MP4 file
        'format': 'best[ext=mp4]/best',  # Get best single format in mp4, or best overall if no mp4
        'paths': {'home': output_dir},
        'outtmpl': '%(title)s.%(ext)s',
        'progress_hooks': [progress_hook],
        'noplaylist': True,  # Only download single video, not playlist
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Download completed: {filename}")
            return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Get URL from command line argument
        url = sys.argv[1]
        output_dir = sys.argv[2] if len(sys.argv) > 2 else None
        download_mp4(url, output_dir)
    else:
        # Ask for URL
        url = input("Enter YouTube URL: ")
        download_mp4(url) 