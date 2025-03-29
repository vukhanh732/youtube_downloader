# YouTube Downloader

A simple desktop YouTube downloader built with **CustomTkinter** and **yt-dlp**. The included **setup.bat** script installs Python (if needed), required dependencies, FFmpeg (via winget), and then builds a standalone `.exe` file in the current folder.

## Features

- **Download YouTube Videos**: Select MP4, MP3, or WAV.
- **Quality Options**: Best, 1080p, 720p, 480p, or audio only.
- **Animated Download Button**: Changes from text to an icon on hover.
- **One-Click Setup**: The `setup.bat` file handles everything automatically on Windows.

## Getting Started

1. **Clone or Download** this repository to your Windows PC.
2. **Run `setup.bat`**:
   - Double-click `setup.bat` **as Administrator** (right-click → “Run as administrator”).
   - The script will:
     1. Check/install Python 3.12 (via winget).
     2. Upgrade pip and install `customtkinter`, `yt-dlp`, `pillow`, and `pyinstaller`.
     3. Check/install FFmpeg (via winget).
     4. Build the `.exe` in the current folder.
     5. Create a desktop shortcut with your custom icon.

3. **Use the Executable**:
   - Look for `youtube_downloader.exe` in the same folder after the script finishes.
   - A desktop shortcut named **“YouTube Downloader.lnk”** is also created (if the script succeeds).
