# MediaRefinery

**Media File Organizer and Renamer**

Refine and polish your media files effortlessly `[Writing smarter names for your files by using TheMovieDB (TMDB)]`

This script organizes and renames media files based on metadata fetched from the TMDB API and media file details extracted using `ffprobe`. It supports various video file formats and ensures consistent naming conventions for easy organization.

---

## Features
- Automatically fetches metadata from TMDB using file names or directory names.
- Extracts media file details (resolution, codec, etc.) using `ffprobe`.
- Handles various naming conventions for TV shows and movies.
- Works with all video file formats.
- Prompts the user only when necessary (e.g., when the title cannot be determined).

---

## Prerequisites
### Tools
1. **Python 3.6+**
2. **FFmpeg** and **FFprobe**:
   - These tools are required to extract media file details.

#### Install FFmpeg and FFprobe
##### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install ffmpeg
```

##### macOS (Homebrew)
```bash
brew install ffmpeg
```

##### Windows
1. Download FFmpeg from the [official website](https://ffmpeg.org/download.html).
2. Extract the files.
3. Add the `bin` directory to your system's PATH environment variable.

##### Verify Installation
Run the following commands to confirm installation:
```bash
ffmpeg -version
ffprobe -version
```

---

## Installation
1. Clone or download this repository.
2. Navigate to the project directory.
3. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage
1. Place the script in the directory containing the media files or specify the target directory in the script.
2. Run the script:
   ```bash
   python script_name.py
   ```
3. If the script cannot determine the media title from the filename, it will fallback to the directory name and prompt for confirmation.

---

## Supported Features
- Supports all video file formats (`.mkv`, `.mp4`, `.avi`, etc.).
- Extracts detailed metadata:
  - Resolution
  - Video codec
  - Audio codec
- Renames files using the following format:
  ```
  {CleanTitle}_{ReleaseYear}_tmdb-{TmdbId}_S{Season}E{Episode}_{Resolution}_{VideoCodec}_{AudioCodec}.{Extension}
  ```

---

## Example Workflow
1. **Before**:
   ```
   doctor.who.s01e07.mkv
   ```
2. **After**:
   ```
   Doctor_Who_2023_tmdb-12345_S01E07_1080p_h264_aac.mkv
   ```

---

## Notes
- Ensure `ffmpeg` and `ffprobe` are installed and available in the system PATH.
- The script relies on the TMDB API for accurate metadata. Ensure the API key is set in the script.


