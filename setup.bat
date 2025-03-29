@echo off
echo =====================================
echo YouTube Downloader Setup Script
echo =====================================
echo.

REM ------------------------------
REM Step 1: Check & Install Python via winget if needed
REM ------------------------------
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Installing Python 3.12 via winget...
    winget install --id=Python.Python.3.12 -e --silent
    if %errorlevel% neq 0 (
        echo Failed to install Python via winget. Please install it manually.
        pause
        exit /b 1
    )
    echo Python installed successfully.
    timeout /t 10
) else (
    echo Python is already installed.
)
echo.

REM ------------------------------
REM Step 2: Upgrade pip and install required packages
REM ------------------------------
echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing required packages (customtkinter, yt-dlp, pillow, pyinstaller)...
python -m pip install customtkinter yt-dlp pillow pyinstaller
echo.

REM ------------------------------
REM Step 3: Check & Install FFmpeg via winget if needed
REM ------------------------------
echo Checking for FFmpeg...
where ffmpeg >nul 2>&1
if %errorlevel% neq 0 (
    echo FFmpeg not found.
    echo Installing FFmpeg via winget...
    winget install --id=Gyan.FFmpeg -e --silent
    if %errorlevel% neq 0 (
        echo Failed to install FFmpeg via winget.
        echo Please install FFmpeg manually from https://ffmpeg.org/download.html
        pause
    ) else (
        echo FFmpeg installed successfully.
    )
) else (
    echo FFmpeg is already installed.
)
echo.

REM ------------------------------
REM Step 4: Build the standalone executable with PyInstaller in the current folder
REM ------------------------------
echo Building the executable with PyInstaller...
python -m PyInstaller --onefile --windowed --distpath . youtube_downloader.py
if %errorlevel% neq 0 (
    echo Build failed.
    pause
    exit /b 1
)
echo.
echo Build complete! The executable is now in the current folder.
echo.

REM ------------------------------
REM Step 5: Create Desktop Shortcut Using PowerShell
REM ------------------------------
echo Creating desktop shortcut...
powershell -command "$s = New-Object -ComObject WScript.Shell; $sc = $s.CreateShortcut('%USERPROFILE%\Desktop\YouTube Downloader.lnk'); $sc.TargetPath = '%cd%\youtube_downloader.exe'; $sc.IconLocation = '%cd%\youtube.ico'; $sc.Save()"
if %errorlevel% neq 0 (
    echo Failed to create desktop shortcut.
) else (
    echo Desktop shortcut created successfully.
)
echo.
pause
