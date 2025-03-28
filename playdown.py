import os
import sys
import threading
import re
import time
import webbrowser
import subprocess
from pathlib import Path
from urllib.parse import urlparse, parse_qs

import customtkinter as ctk
from PIL import Image, ImageTk
import yt_dlp
try:
    import ffmpeg
    FFMPEG_IMPORTED = True
except ImportError:
    FFMPEG_IMPORTED = False
from tqdm import tqdm

class PlaydownApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure the window
        self.title("Playdown")
        self.geometry("800x600")
        self.minsize(800, 600)
        
        # Set the appearance mode and color theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create variables
        self.url_var = ctk.StringVar()
        self.download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        self.download_in_progress = False
        self.video_info = None
        self.is_playlist = False
        self.playlist_videos = []
        self.selected_videos = []
        self.current_download_progress = 0
        self.ffmpeg_available = self.check_ffmpeg()
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create header
        self.create_header()
        
        # Create URL input area
        self.create_url_input()
        
        # Create settings area
        self.create_settings()
        
        # Create content area (video details or playlist)
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create video details area
        self.video_details_frame = ctk.CTkFrame(self.content_frame)
        
        # Create playlist area
        self.playlist_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.playlist_checkboxes = []
        
        # Create status bar
        self.create_status_bar()
        
        # Check FFmpeg
        if not self.ffmpeg_available:
            self.show_ffmpeg_warning()
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available on the system"""
        try:
            # Try using subprocess to run ffmpeg -version
            result = subprocess.run(
                ['ffmpeg', '-version'], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                text=True,
                timeout=2,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            return result.returncode == 0
        except Exception:
            return False
    
    def show_ffmpeg_warning(self):
        """Show a warning dialog when FFmpeg is not available"""
        warning_window = ctk.CTkToplevel(self)
        warning_window.title("FFmpeg Not Found")
        warning_window.geometry("500x320")
        warning_window.resizable(False, False)
        warning_window.transient(self)
        warning_window.grab_set()
        
        # Add content to the warning window
        frame = ctk.CTkFrame(warning_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        title = ctk.CTkLabel(
            frame,
            text="FFmpeg Not Installed",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title.pack(pady=(0, 10))
        
        message = ctk.CTkLabel(
            frame,
            text="FFmpeg is required to convert videos to MP3 format.\n\n"
                "Without FFmpeg, you can still download videos in MP4 format,\n"
                "but audio conversion will not work.\n\n"
                "Would you like to download FFmpeg now?",
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        message.pack(pady=10)
        
        button_frame = ctk.CTkFrame(frame)
        button_frame.pack(fill="x", pady=10)
        
        download_ffmpeg = ctk.CTkButton(
            button_frame,
            text="Download FFmpeg",
            font=ctk.CTkFont(size=14),
            command=self.open_ffmpeg_download
        )
        download_ffmpeg.pack(side="left", padx=10)
        
        continue_button = ctk.CTkButton(
            button_frame,
            text="Continue Without FFmpeg",
            font=ctk.CTkFont(size=14),
            command=warning_window.destroy
        )
        continue_button.pack(side="right", padx=10)
        
        # Disable MP3 option if FFmpeg is not available
        if hasattr(self, 'mp3_radio'):
            self.mp3_radio.configure(state="disabled")
            self.format_var.set("mp4")
    
    def open_ffmpeg_download(self):
        """Open FFmpeg download page in the default browser"""
        webbrowser.open("https://ffmpeg.org/download.html")
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # App title
        title_label = ctk.CTkLabel(
            header_frame, 
            text="Playdown", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=10)
        
        # App subtitle
        subtitle_label = ctk.CTkLabel(
            header_frame, 
            text="YouTube Video & Playlist Downloader",
            font=ctk.CTkFont(size=14)
        )
        subtitle_label.pack(side="left", padx=10)
    
    def create_url_input(self):
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.pack(fill="x", pady=10)
        
        url_label = ctk.CTkLabel(
            url_frame, 
            text="Video or Playlist URL:",
            font=ctk.CTkFont(size=14)
        )
        url_label.pack(side="left", padx=10)
        
        url_entry = ctk.CTkEntry(
            url_frame, 
            textvariable=self.url_var,
            width=400,
            height=30,
            font=ctk.CTkFont(size=14)
        )
        url_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        fetch_button = ctk.CTkButton(
            url_frame, 
            text="Fetch Info",
            font=ctk.CTkFont(size=14),
            command=self.fetch_info
        )
        fetch_button.pack(side="left", padx=10)
    
    def create_settings(self):
        settings_frame = ctk.CTkFrame(self.main_frame)
        settings_frame.pack(fill="x", pady=10)
        
        # Output format options
        format_label = ctk.CTkLabel(
            settings_frame, 
            text="Format:",
            font=ctk.CTkFont(size=14)
        )
        format_label.pack(side="left", padx=10)
        
        # Default format is mp4 if FFmpeg is not available
        default_format = "mp4" if not self.ffmpeg_available else "mp3"
        self.format_var = ctk.StringVar(value=default_format)
        
        self.mp3_radio = ctk.CTkRadioButton(
            settings_frame, 
            text="MP3",
            variable=self.format_var,
            value="mp3",
            font=ctk.CTkFont(size=14),
            state="normal" if self.ffmpeg_available else "disabled"
        )
        self.mp3_radio.pack(side="left", padx=10)
        
        mp4_radio = ctk.CTkRadioButton(
            settings_frame, 
            text="MP4",
            variable=self.format_var,
            value="mp4",
            font=ctk.CTkFont(size=14)
        )
        mp4_radio.pack(side="left", padx=10)
        
        # Download path
        path_label = ctk.CTkLabel(
            settings_frame, 
            text="Save to:",
            font=ctk.CTkFont(size=14)
        )
        path_label.pack(side="left", padx=10)
        
        self.path_display = ctk.CTkLabel(
            settings_frame, 
            text=self.download_path,
            font=ctk.CTkFont(size=14)
        )
        self.path_display.pack(side="left", padx=10)
        
        browse_button = ctk.CTkButton(
            settings_frame, 
            text="Browse",
            font=ctk.CTkFont(size=14),
            command=self.browse_directory
        )
        browse_button.pack(side="left", padx=10)
    
    def create_status_bar(self):
        self.status_frame = ctk.CTkFrame(self.main_frame)
        self.status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ctk.CTkLabel(
            self.status_frame, 
            text="Ready",
            font=ctk.CTkFont(size=14)
        )
        self.status_label.pack(side="left", padx=10)
        
        self.progress_bar = ctk.CTkProgressBar(self.status_frame)
        self.progress_bar.pack(side="left", padx=10, fill="x", expand=True)
        self.progress_bar.set(0)
        
        self.download_button = ctk.CTkButton(
            self.status_frame, 
            text="Download",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.start_download,
            state="disabled"
        )
        self.download_button.pack(side="right", padx=10)
    
    def fetch_info(self):
        url = self.url_var.get().strip()
        if not url:
            self.show_status("Please enter a valid URL", "error")
            return
        
        self.show_status("Fetching video information...", "info")
        self.download_button.configure(state="disabled")
        self.progress_bar.set(0)
        
        # Clear previous content
        for widget in self.content_frame.winfo_children():
            widget.pack_forget()
        
        # Start fetching in a separate thread
        threading.Thread(target=self._fetch_info_thread, args=(url,), daemon=True).start()
    
    def _fetch_info_thread(self, url):
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'ignoreerrors': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                if 'entries' in info:  # It's a playlist
                    self.is_playlist = True
                    self.playlist_videos = list(info['entries'])
                    self.after(100, self.display_playlist_info)
                else:  # It's a single video
                    self.is_playlist = False
                    self.video_info = info
                    self.after(100, self.display_video_info)
                
                self.after(100, lambda: self.show_status("Ready to download", "success"))
                self.after(100, lambda: self.download_button.configure(state="normal"))
                
        except Exception as e:
            self.after(100, lambda: self.show_status(f"Error: {str(e)}", "error"))
    
    def display_video_info(self):
        self.video_details_frame.pack(fill="both", expand=True)
        
        # Clear previous content
        for widget in self.video_details_frame.winfo_children():
            widget.destroy()
        
        # Video title
        title_label = ctk.CTkLabel(
            self.video_details_frame, 
            text=self.video_info.get('title', 'Unknown Title'),
            font=ctk.CTkFont(size=18, weight="bold"),
            wraplength=700
        )
        title_label.pack(pady=(20, 10), padx=20)
        
        # Video details
        details_frame = ctk.CTkFrame(self.video_details_frame)
        details_frame.pack(fill="x", padx=20, pady=10)
        
        # Channel
        channel_label = ctk.CTkLabel(
            details_frame, 
            text=f"Channel: {self.video_info.get('uploader', 'Unknown')}",
            font=ctk.CTkFont(size=14)
        )
        channel_label.pack(anchor="w", padx=10, pady=5)
        
        # Duration
        duration = self.video_info.get('duration', 0)
        minutes, seconds = divmod(int(duration), 60)
        hours, minutes = divmod(minutes, 60)
        
        duration_text = f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"
        duration_label = ctk.CTkLabel(
            details_frame, 
            text=f"Duration: {duration_text}",
            font=ctk.CTkFont(size=14)
        )
        duration_label.pack(anchor="w", padx=10, pady=5)
    
    def display_playlist_info(self):
        self.playlist_frame.pack(fill="both", expand=True)
        
        # Clear previous content
        for widget in self.playlist_frame.winfo_children():
            widget.destroy()
        
        self.playlist_checkboxes = []
        self.selected_videos = []
        
        # Header with select all option
        header_frame = ctk.CTkFrame(self.playlist_frame)
        header_frame.pack(fill="x", padx=5, pady=5)
        
        self.select_all_var = ctk.BooleanVar(value=True)
        select_all_cb = ctk.CTkCheckBox(
            header_frame,
            text="Select All",
            variable=self.select_all_var,
            command=self.toggle_select_all,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        select_all_cb.pack(side="left", padx=10)
        
        count_label = ctk.CTkLabel(
            header_frame,
            text=f"Total: {len(self.playlist_videos)} videos",
            font=ctk.CTkFont(size=14)
        )
        count_label.pack(side="right", padx=10)
        
        # Display each video in the playlist
        for i, video in enumerate(self.playlist_videos):
            if not video:  # Skip unavailable videos
                continue
                
            video_frame = ctk.CTkFrame(self.playlist_frame)
            video_frame.pack(fill="x", padx=5, pady=2)
            
            # Create checkbox for selection
            var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(
                video_frame,
                text="",
                variable=var,
                width=20
            )
            checkbox.pack(side="left", padx=5)
            
            # Track checkbox and video info
            self.playlist_checkboxes.append((var, video))
            self.selected_videos.append(video)
            
            # Video number and title
            title_text = f"{i+1}. {video.get('title', 'Unknown')}"
            title_label = ctk.CTkLabel(
                video_frame,
                text=title_text,
                font=ctk.CTkFont(size=14),
                anchor="w",
                wraplength=700
            )
            title_label.pack(side="left", padx=5, fill="x", expand=True)
            
            # Duration
            duration = video.get('duration', 0) or 0
            minutes, seconds = divmod(int(duration), 60)
            hours, minutes = divmod(minutes, 60)
            
            duration_text = f"{hours:02}:{minutes:02}:{seconds:02}" if hours > 0 else f"{minutes:02}:{seconds:02}"
            duration_label = ctk.CTkLabel(
                video_frame,
                text=duration_text,
                font=ctk.CTkFont(size=14),
                width=60
            )
            duration_label.pack(side="right", padx=10)
    
    def toggle_select_all(self):
        select_all = self.select_all_var.get()
        
        self.selected_videos = []
        for var, video in self.playlist_checkboxes:
            var.set(select_all)
            if select_all:
                self.selected_videos.append(video)
    
    def browse_directory(self):
        path = ctk.filedialog.askdirectory(initialdir=self.download_path)
        if path:
            self.download_path = path
            self.path_display.configure(text=self.download_path)
    
    def start_download(self):
        if self.download_in_progress:
            return
            
        if self.is_playlist:
            # Update selected videos based on checkboxes
            self.selected_videos = []
            for var, video in self.playlist_checkboxes:
                if var.get():
                    self.selected_videos.append(video)
            
            if not self.selected_videos:
                self.show_status("No videos selected", "error")
                return
                
            self.show_status(f"Downloading {len(self.selected_videos)} videos...", "info")
        else:
            if not self.video_info:
                self.show_status("No video information available", "error")
                return
            self.show_status("Downloading video...", "info")
        
        self.download_in_progress = True
        self.download_button.configure(state="disabled")
        self.progress_bar.set(0)
        
        # Start downloading in a separate thread
        threading.Thread(target=self._download_thread, daemon=True).start()
    
    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            # Calculate download progress
            if 'total_bytes' in d and d['total_bytes'] > 0:
                progress = d['downloaded_bytes'] / d['total_bytes']
            elif 'total_bytes_estimate' in d and d['total_bytes_estimate'] > 0:
                progress = d['downloaded_bytes'] / d['total_bytes_estimate']
            else:
                # Can't determine progress, use indeterminate indicator
                progress = -1
                
            # Update progress in the UI thread
            self.current_download_progress = progress
            self.after(100, lambda p=progress: self._update_progress_ui(p))
            
        elif d['status'] == 'finished':
            # Download finished, show converting status
            self.after(100, lambda: self.show_status("Converting media...", "info"))
        
        elif d['status'] == 'error':
            error_msg = d.get('error', 'Unknown error')
            self.after(100, lambda msg=error_msg: self.show_status(f"Error: {msg}", "error"))
    
    def _update_progress_ui(self, progress):
        if progress >= 0:
            self.progress_bar.set(progress)
        else:
            # Could implement indeterminate progress indicator here
            pass
    
    def _download_thread(self):
        try:
            format_option = self.format_var.get()
            
            # Check if MP3 was selected but FFmpeg is not available
            if format_option == "mp3" and not self.ffmpeg_available:
                self.after(100, lambda: self.show_status("FFmpeg not found. Using MP4 format instead.", "warning"))
                format_option = "mp4"
            
            if self.is_playlist:
                total_videos = len(self.selected_videos)
                
                for i, video in enumerate(self.selected_videos):
                    video_url = video.get('webpage_url') or video.get('url')
                    if not video_url:
                        continue
                        
                    self.after(100, lambda i=i, total=total_videos, title=video.get('title', ''): 
                        self.show_status(f"Downloading video {i+1}/{total}: {title}", "info"))
                        
                    # Download one video
                    self._download_single_video(video_url, format_option)
                    
                    # Update overall playlist progress
                    playlist_progress = (i + 1) / total_videos
                    self.after(100, lambda p=playlist_progress: self.progress_bar.set(p))
                
                self.after(100, lambda: self.show_status("All downloads completed", "success"))
            else:
                video_url = self.video_info.get('webpage_url') or self.video_info.get('url')
                self._download_single_video(video_url, format_option)
                self.after(100, lambda: self.show_status("Download completed", "success"))
            
        except Exception as e:
            self.after(100, lambda: self.show_status(f"Error: {str(e)}", "error"))
        finally:
            self.after(100, lambda: self.progress_bar.set(1.0))
            self.after(100, lambda: setattr(self, 'download_in_progress', False))
            self.after(100, lambda: self.download_button.configure(state="normal"))
    
    def _download_single_video(self, video_url, format_option):
        # Reset progress for this video
        self.after(100, lambda: self.progress_bar.set(0))
        self.current_download_progress = 0
        
        if format_option == "mp3":
            ydl_opts = {
                'format': 'bestaudio/best',
                'paths': {'home': self.download_path},
                'outtmpl': '%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'progress_hooks': [self._progress_hook],
                'verbose': False,
            }
        else:  # mp4
            if self.ffmpeg_available:
                # Use format merging if FFmpeg is available
                ydl_opts = {
                    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                    'paths': {'home': self.download_path},
                    'outtmpl': '%(title)s.%(ext)s',
                    'progress_hooks': [self._progress_hook],
                    'verbose': False,
                }
            else:
                # Use a single format to avoid FFmpeg requirements
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'paths': {'home': self.download_path},
                    'outtmpl': '%(title)s.%(ext)s',
                    'progress_hooks': [self._progress_hook],
                    'verbose': False,
                }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
        except Exception as e:
            self.after(100, lambda e=e: self.show_status(f"Download error: {str(e)}", "error"))
            raise e
    
    def show_status(self, message, message_type="info"):
        color_map = {
            "info": "light blue",
            "success": "green",
            "error": "red",
            "warning": "orange"
        }
        
        self.status_label.configure(
            text=message,
            text_color=color_map.get(message_type, "white")
        )

if __name__ == "__main__":
    app = PlaydownApp()
    app.mainloop()
