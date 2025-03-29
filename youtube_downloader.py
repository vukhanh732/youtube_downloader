import customtkinter
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
import platform
from PIL import Image, ImageTk
from yt_dlp import YoutubeDL

# Set global appearance for CustomTkinter
customtkinter.set_appearance_mode("Dark")  # "System", "Dark", or "Light"
customtkinter.set_default_color_theme("blue")

# -------------------------------
# Custom Animated Download Button
# -------------------------------
class AnimatedDownloadButton(customtkinter.CTkFrame):
    def __init__(self, master, text="Download", command=None, **kwargs):
        # Set button dimensions
        width = 100
        height = 35
        super().__init__(master, width=width, height=height, corner_radius=5, **kwargs)
        self.default_bg = "#1163ff"
        self.hover_bg = "#6c18ff"
        self.configure(fg_color=self.default_bg)  # Background color
        self.command = command

        # Create label for the text (normal state)
        self.text_label = customtkinter.CTkLabel(
            self, text=text, fg_color=self.default_bg, text_color="white", font=("Arial", 10)
        )
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

        # Create label for the icon (hover state) - a down arrow
        self.icon_label = customtkinter.CTkLabel(
            self, text="⬇", fg_color=self.default_bg, text_color="white", font=("Arial", 12)
        )
        # Initially hidden (placed off-frame)
        self.icon_label.place_forget()

        # Bind mouse events
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_click)
        self.text_label.bind("<Enter>", self.on_enter)
        self.text_label.bind("<Leave>", self.on_leave)
        self.text_label.bind("<Button-1>", self.on_click)
        self.icon_label.bind("<Enter>", self.on_enter)
        self.icon_label.bind("<Leave>", self.on_leave)
        self.icon_label.bind("<Button-1>", self.on_click)

    def on_enter(self, event):
        # Change background color to hover state
        self.configure(fg_color=self.hover_bg)
        # Hide text and show icon
        self.text_label.place_forget()
        self.icon_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_leave(self, event):
        # Revert background color
        self.configure(fg_color=self.default_bg)
        # Hide icon and show text
        self.icon_label.place_forget()
        self.text_label.place(relx=0.5, rely=0.5, anchor="center")

    def on_click(self, event):
        if self.command:
            self.command()

# -------------------------------
# Main Application Class
# -------------------------------
class YouTubeDownloaderApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("YouTube Downloader")
        self.geometry("700x400")

        # --- Set the app icon ---
        if platform.system() == "Windows":
            try:
                self.iconbitmap("youtube.ico")
            except Exception as e:
                print("Could not set .ico icon:", e)
        else:
            try:
                yt_icon_img = Image.open("youtube.ico")
                yt_icon_img = yt_icon_img.resize((64, 64), Image.LANCZOS)
                self.iconphoto(False, ImageTk.PhotoImage(yt_icon_img))
            except Exception as e:
                print("Could not set PNG icon:", e)

        # Default download folder is the current working directory
        self.download_path = tk.StringVar(value=os.getcwd())

        # Main container frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # 1) URL Label + Entry
        self.url_label = customtkinter.CTkLabel(self.main_frame, text="YouTube URL:")
        self.url_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10,5))

        self.url_entry = customtkinter.CTkEntry(
            self.main_frame,
            width=400,
            placeholder_text="https://www.youtube.com/watch?v=..."
        )
        self.url_entry.grid(row=0, column=1, columnspan=2, sticky="ew", padx=10, pady=(10,5))

        # 2) Download Path Label + Entry + Browse Button
        self.path_label = customtkinter.CTkLabel(self.main_frame, text="Download Folder:")
        self.path_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        self.path_entry = customtkinter.CTkEntry(self.main_frame, textvariable=self.download_path, width=350)
        self.path_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        self.browse_button = customtkinter.CTkButton(self.main_frame, text="Browse...", command=self.browse_path)
        self.browse_button.grid(row=1, column=2, sticky="e", padx=10, pady=5)

        # 3) Format Selection
        self.format_label = customtkinter.CTkLabel(self.main_frame, text="Format:")
        self.format_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        self.format_options = ["mp4", "mp3", "wav"]
        self.format_var = tk.StringVar(value=self.format_options[0])
        self.format_combobox = customtkinter.CTkComboBox(
            self.main_frame,
            values=self.format_options,
            variable=self.format_var
        )
        self.format_combobox.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # 4) Quality Selection
        self.quality_label = customtkinter.CTkLabel(self.main_frame, text="Quality:")
        self.quality_label.grid(row=3, column=0, sticky="w", padx=10, pady=5)

        self.quality_options = ["best", "1080p", "720p", "480p", "audio only"]
        self.quality_var = tk.StringVar(value=self.quality_options[0])
        self.quality_combobox = customtkinter.CTkComboBox(
            self.main_frame,
            values=self.quality_options,
            variable=self.quality_var
        )
        self.quality_combobox.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        # 5) Download Button using our custom animated button widget
        self.download_button = AnimatedDownloadButton(
            self.main_frame,
            text="Download",
            command=self.start_download
        )
        self.download_button.grid(row=4, column=0, columnspan=3, pady=(10,5))

        # 6) Progress Bar
        self.progress_bar = customtkinter.CTkProgressBar(self.main_frame, mode="determinate")
        self.progress_bar.grid(row=5, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.progress_bar.set(0)

        # 7) Progress Label
        self.progress_label = customtkinter.CTkLabel(self.main_frame, text="")
        self.progress_label.grid(row=6, column=0, columnspan=3, padx=10, pady=5)

        # Allow the second column to expand
        self.main_frame.grid_columnconfigure(1, weight=1)

    def browse_path(self):
        """Open a directory chooser and set the download path."""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.download_path.set(folder_selected)

    def start_download(self):
        """Triggered by the Download button; starts download in a background thread."""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a valid YouTube URL.")
            return

        self.progress_bar.set(0)
        self.progress_label.configure(text="Starting download...")

        threading.Thread(target=self.download_video, args=(url,), daemon=True).start()

    def download_video(self, url):
        """Builds yt-dlp options and performs the download."""
        fmt = self.format_var.get()
        quality = self.quality_var.get()
        out_path = self.download_path.get()

        ydl_opts = self.build_ydl_opts(fmt, quality, out_path)

        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.on_download_complete()
        except Exception as e:
            self.on_download_error(str(e))

    def build_ydl_opts(self, fmt, quality, out_path):
        """
        Returns a dictionary of options for YoutubeDL based on user selections.
        Ensures that merging/conversion happens so that no leftover files remain.
        """
        ydl_opts = {
            'outtmpl': os.path.join(out_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
            'logger': YTLogger(self),
            'progress_hooks': [self.progress_hook],
            'postprocessors': [],
            'keepvideo': False,
        }

        if fmt == "mp4":
            ydl_opts['merge_output_format'] = 'mp4'
        else:
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegExtractAudio',
                'preferredcodec': fmt,
            })

        if quality == "best":
            if fmt == "mp4":
                ydl_opts['format'] = 'bestvideo+bestaudio/best'
        elif quality == "1080p":
            if fmt == "mp4":
                ydl_opts['format'] = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]'
            else:
                ydl_opts['format'] = 'bestaudio/best'
        elif quality == "720p":
            if fmt == "mp4":
                ydl_opts['format'] = 'bestvideo[height<=720]+bestaudio/best[height<=720]'
            else:
                ydl_opts['format'] = 'bestaudio/best'
        elif quality == "480p":
            if fmt == "mp4":
                ydl_opts['format'] = 'bestvideo[height<=480]+bestaudio/best[height<=480]'
            else:
                ydl_opts['format'] = 'bestaudio/best'
        elif quality == "audio only":
            ydl_opts['format'] = 'bestaudio/best'
            if fmt == "mp4":
                ydl_opts['postprocessors'].append({
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                })

        if fmt == "mp4":
            ydl_opts['postprocessors'].append({
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            })

        return ydl_opts

    def progress_hook(self, d):
        """Called by yt-dlp to report download progress."""
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0.0%')
            try:
                percent = float(percent_str.replace('%', '').strip())
            except ValueError:
                percent = 0.0
            self.set_progress(percent)
        elif d['status'] == 'finished':
            self.set_progress(100)

    def set_progress(self, percent):
        """Update the progress bar and label."""
        self.progress_bar.set(percent / 100.0)
        self.progress_label.configure(text=f"{percent:.2f}%")
        self.update_idletasks()

    def on_download_complete(self):
        """Called when download finishes successfully."""
        self.progress_label.configure(text="Download completed!")
        messagebox.showinfo("Success", "Download completed successfully!")

    def on_download_error(self, error_msg):
        """Called if the download fails."""
        self.progress_label.configure(text="Download failed!")
        messagebox.showerror("Error", f"An error occurred:\n{error_msg}")

class YTLogger:
    """Custom logger for yt-dlp."""
    def __init__(self, app):
        self.app = app
    def debug(self, msg): pass
    def info(self, msg): pass
    def warning(self, msg): pass
    def error(self, msg): pass

if __name__ == "__main__":
    app = YouTubeDownloaderApp()
    app.mainloop()
