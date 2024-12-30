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




