# Sorcery
## Automated Video Highlight Generator 

Upload long-form footage, target a specific keyword (e.g., "System Design"), and get a stitched clip of every moment that word was mentioned.

# The Origin 🧙🏿
The idea started whilst watching the *Merlin* series, hoping to find a montage of the word  "sorcery" being mispronounced. When I couldn't find one, I realised the manual effort to clip specific moments from hours of footage is a universal problem. Whether it's for interview portfolios, lecture highlights, or content curation, the tool to automate this didn't exist. I built it.

# Tech Stack 🛠️
- **Python**: Core logic and orchestration
- **Whisper (OpenAI)**: Robust ASR for accurate transcript-to-timestamp mapping.
- **MoviePY**: Video manipulation, subclipping and concatenation.
- **Streamlit**: Rapid UI for file uploads and immediate feedback.
- **Tempfile**: Secure, ephemeral file handling for uploaded assets.

# Installation ⚙️
```bash```
## Clone repo
git clone - https://github.com/pgik13/sorcery

cd sorcery

## Create virtual environment
python -m venv venv
source venv/bin/activate 

**Windows: venv/Scripts/activate**

## Install dependencies
pip install -r requirements.txt

**Ensure ffmpeg is installed and in PATH (required by MoviePy)**

# Usage 🎬
1. Upload .mp4 files (Max 50MB per file)
2. Enter target word
3. Click "Complie Video"
4. Download a single .mp4 file containing all matching segments stitched together


# Architecture & Challenges 🧠
1. **Robust ASR parsing (Type Safety)**
   
   ***Challenge***: Whisper's ```transcribe()``` method returns segments as ```dict```s in some versions and ```namedtuple```s in others, causing ```TypeError: tuple indices must be integers or slices, not str``` when accessing keys

   ***Solution***: Implement a dual-format handler in ```wordMatch()``` that checks ```isinstance(segment, dict)``` and has attribute access (```segment.text```) for namedtuples as a back up. This ensured compatibility across environments

2. **File Handle Lifecycle and Memory Mangement**

   ***Challenge**: ```ValueError: I/O operation on closed file``` occured when ```MoviePy``` tried to read from temp files that were deleted while ```VideoFileClip``` objects still held open file handles.

   ***Solution***:

   ***Materialise subclips***: Subclips are rendered to new temp files immediately instead of holding open references to original temp file

   **Decoupled lifecycle**: Original uploads are deleted after subclip is generated. Final concatenation reads from the newly created stable subclip files

   **Explicit Cleanup**: All temp files are tracked in a list and are only deleted after the final video has been complied and all handles are closed

3. **Streamlit State and Progress**

   **Challenge**: ```uploadedFiles``` iterator consumption and progress bar logic.

   **Solution**:
   Store file count before iteration to prevent ```TypeError``` on re-reading the iterator. Implemented robust error handling to ensure temp files are cleaned up even if processing fails mid-stream

# Known limitations ⚠️

- **File size**: Hard limit of 50MB per file due to Streamlit upload constraints and memory usage 
- **Processing Time**: Large batches of videos may timme out without server backing. Sequential processing
- **Audio codecs**: Requires _libx264_ and _aac_ support (standard ffmpeg install)

# Potential updates 🚀

- **Buffer selection**: Add configurable seconds before and after the keyword for better context
- **Async Processing**: Migrate to Celery/Redis for large file processing
- **Multi-Language**: Support for non-English transcripts

# Contact

Built by Pius Gikunoo

**LinkedIn**: https://www.linkedin.com/in/pius-gikunoo-2693b6223/

**GitHub**: https://github.com/pgik13
