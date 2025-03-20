# Spotify GUI Overlay

A customizable Spotify overlay for Linux and Windows that displays current track information and playback controls.

![Spotify Gif](https://github.com/adithyanraj03/GUI-Overlay-For-Spotify-LINUX-WINDOWS/blob/main/2.gif)

## ✨ Features

- 🎵 Displays album art, song title, and artist
- 🎚️ Playback controls (previous, play/pause, next)
- 🌈 Animated music visualization
- 🖱️ Draggable overlay window
- 🖼️ Watermarked album art
  
  <br>
![Spotify Overlay Screenshot](https://github.com/adithyanraj03/GUI-Overlay-For-Spotify-LINUX-WINDOWS/blob/main/1.png)

## 🛠️ Requirements

- Python 3.6+
- GTK 3.0
- Spotify desktop application

## 🚀 Installation

### Linux

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/spotify-overlay.git
   cd spotify-overlay
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

### Windows

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/spotify-overlay.git
   cd spotify-overlay
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 🎮 Usage

### Linux

1. Run the .desktop file:
   ```bash
   ./spotify-overlay.desktop
   ```

   If the .desktop file doesn't work, run the launch script:
   ```bash
   ./launch_spotify_with_overlay.sh
   ```

   Alternatively, you can run the Python script directly:
   ```bash
   python3 dist/main.py
   ```

### Windows

1. Run the batch file:
   ```bash
   windows.bat
   ```

   Or create a shortcut to the batch file and run it.

2. If needed, modify the Spotify location in the batch file:
   ```bash
   start "" "C:\Users\YourUsername\AppData\Roaming\Spotify\Spotify.exe"
   ```
3. Alternatively, you can run the Python script directly:
   ```bash
   python dist/main.py
   ```


## 🎨 Customization

For Customizations Contact me 😄 click: [Email](https://mail.google.com/mail/?view=cm&fs=1&to=adithyanraj03@gmail.com&su=Spotify%20GUI%20Overlay&body=Hello%20Developer%20Adithya,%0A%0AI%20came%20across%20your%20Git%20repository%20for%20the%20Spotify%20GUI%20Overlay%20and%20wanted%20to%20reach%20out.%0A%0AI'm%20interested%20in%20discussing%20some%20ideas.%0A%0ABest,%0A[Your%20Name])


## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
