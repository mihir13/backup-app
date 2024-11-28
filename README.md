# Backup App

This is a desktop application for Mac that allows users to back up important directories such as 'Downloads', 'Documents', and 'Photos' to a home server.

## Features
- Select directories or files to back up using native macOS dialogs
- Choose a restore directory for backups
- Monitor backup progress with a progress bar (shown for transfers estimated to take more than 10 seconds)
- Toggle between light and dark mode for the application interface
- Displays company logo and name in the UI
- Conditional display of dialogs and progress bar matching the current theme
- Efficient local file transfer using `shutil`

## Requirements
- Python 3.x
- PyQt5

## Setup
1. Install the required packages: `pip install -r requirements.txt`
2. Run the application: `python main.py`

## Usage
- Use the 'Select Backup Path' button to choose files or directories to back up.
- Use the 'Select Restore Path' button to choose where to restore the backups.
- Click 'Start Backup' to begin the backup process.
- Use the theme toggle button in the top right corner to switch between light and dark modes.
