```text
    ███████╗██╗██████╗ ██████╗ ██╗     ███████╗    ███╗   ███╗███████╗    ████████╗██╗  ██╗██╗███████╗██╗
    ██╔════╝██║██╔══██╗██╔══██╗██║     ██╔════╝    ████╗ ████║██╔════╝    ╚══██╔══╝██║  ██║██║██╔════╝██║
    █████╗  ██║██║  ██║██║  ██║██║     █████╗      ██╔████╔██║█████╗         ██║   ███████║██║███████╗██║
    ██╔══╝  ██║██║  ██║██║  ██║██║     ██╔══╝      ██║╚██╔╝██║██╔══╝         ██║   ██╔══██║██║╚════██║╚═╝
    ██║     ██║██████╔╝██████╔╝███████╗███████╗    ██║ ╚═╝ ██║███████╗       ██║   ██║  ██║██║███████║██╗
    ╚═╝     ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚══════╝    ╚═╝     ╚═╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝
```

A terminal-based interactive music trivia game! This project uses AI source separation (HTDemucs) to split songs into individual tracks (stems) - Bass, Drums, Guitar, Piano, Vocals, and Other.

In the game, a song starts playing with just a single track (like the bassline). If you can't guess the song, you can add the next track (e.g., drums) into the mix, layering the audio until the full song is playing. See how few tracks you need to guess the song!

## Prerequisites

Before running this project, you need the following installed on your system:

1. **Python 3.8+**
2. **FFmpeg:** Required by `pyglet` and `audio-separator` to decode/encode audio files (like MP3s, M4As, FLACs).
   - **Windows:** Install via `winget install ffmpeg` or download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) and add to your system PATH.
   - **macOS:** `brew install ffmpeg`
   - **Linux:** `sudo apt install ffmpeg`
3. _(Optional but highly recommended)_ **NVIDIA GPU:** For significantly faster song separation.

## Installation

1. Clone or download this repository.
2. Ensure you have the correct PyTorch wheels for your system (the example below uses CUDA 12.8 for GPU acceleration).
3. Install the required Python dependencies:

```bash
# Point pip to the PyTorch index for CUDA support
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

# Install the rest of the requirements
pip install -r requirements.txt
```

## Usage

The project is split into two phases: **Extracting** (adding songs to your database) and **Playing** (the actual game).

### 1. Adding Songs (`extractor.py`)

Before you can play, you need to process at least one audio file. The extractor will isolate the tracks and guide you through setting them up.

```bash
python extractor.py "path/to/your/song.mp3"
```

**During extraction, you will be prompted to:**

1. Enter the Song Title, Artist, Album, and Release Year.
2. Listen to an audition of each extracted track (Bass, Drums, Guitar, Piano, Other, Vocals).
3. Choose whether to include or discard each track (useful if a song has no piano, for example).
4. Define the exact playback order for the game (e.g., start with bass, then drums, then vocals...).

All processed data is saved in a generated `songs/` folder.

### 2. Playing the Game (`main.py`)

Once you have extracted one or more songs, launch the game:

```bash
python main.py
```

A random song from your `songs/` folder will be selected. You will be given the Release Year and Song Length as hints.

**Game Commands:**

- `guess <song name>` - Make a guess (case-insensitive).
- `next` - Layer the next track into the currently playing song.
- `seek mm:ss` - Jump to a specific timestamp in the song (e.g., `seek 01:15`).
- `pause` - Pause playback.
- `resume` - Resume playback.
- `surrender` - Give up and reveal the song details.
- `help` - Show all available commands.
- `stop` - Exit the game completely.

## Note

- **First Run:** The very first time you run `extractor.py`, it will download the HTDemucs AI model weights. This might take a moment depending on your internet speed.

