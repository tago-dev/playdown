import os
import sys
from pathlib import Path
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
        print("Download finished, now converting...")
    elif d['status'] == 'error':
        print(f"Error occurred: {d.get('error')}")

def test_download():
    # Use a short Creative Commons video for testing
    test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"  # Me at the zoo (first YouTube video)
    
    # Set download path
    download_path = os.path.join(os.path.expanduser("~"), "Downloads")
    print(f"Downloading to: {download_path}")
    
    # Configure yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'paths': {'home': download_path},
        'outtmpl': 'test_download.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'progress_hooks': [progress_hook],
    }
    
    # Perform download
    print(f"Downloading {test_url}")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([test_url])
        
        # Check if file exists
        expected_file = os.path.join(download_path, "test_download.mp3")
        if os.path.exists(expected_file):
            print(f"Success! File downloaded to {expected_file}")
            file_size = os.path.getsize(expected_file)
            print(f"File size: {file_size/1024:.1f} KB")
            return True
        else:
            print(f"Error: File not found at {expected_file}")
            return False
    
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    test_download() 