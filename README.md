# YouTube-Notes-Maker

This project provides a Flask backend for downloading audio from YouTube, transcribing the audio, splitting it into chunks, and generating notes using OpenAI's GPT-4o-mini model. The backend provides real-time status updates to the user using Server-Sent Events (SSE).

## Features

- **Download Audio**: Download audio from a YouTube video using `yt-dlp`.
- **Audio Splitting**: Split audio into manageable chunks.
- **Transcription**: Transcribe audio to text using OpenAI's Whisper model.
- **Notes Generation**: Generate insightful notes from the transcription using GPT-4.
- **Real-Time Status Updates**: Receive real-time status updates while processing the audio.

## Technologies Used

- **Python 3**
- **Flask**
- **yt-dlp**: For downloading audio from YouTube.
- **pydub**: For audio processing and splitting.
- **OpenAI API**: For transcription and notes generation.
- **Server-Sent Events (SSE)**: For real-time status updates.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/YouTube-Notes-Maker.git
   cd YouTube-Notes-Maker

   ```

2. **Install dependencies:**

   ```bash
   pip install -U -r requirements.txt
   ```

4. **Set up environment variables:**

   1. Navigate to Your Project Directory
   2. Open the `.env` file with `nano`:

      `nano .env`
5. **Edit the `.env` File:**
      ```
      OPENAI_API_KEY=your-openai-api-key
      ```
6. **Save and Exit:**
      - To save the changes, press Ctrl + O (write out), then press Enter.
      - To exit, press Ctrl + X.

7. **`FFmpeg` Installation**

#### On Windows:

##### Download
Go to the FFmpeg Official Website and download the latest build for Windows.

##### Extract
Extract the downloaded ZIP file to a directory, for example, C:\FFmpeg.

##### Environment Variable:
- Right-click on 'This PC' or 'Computer' on your desktop or File Explorer, and select 'Properties'.

- Click on 'Advanced system settings' and then 'Environment Variables'.

- Under 'System Variables', find and select 'Path', then click 'Edit'.

- Click 'New' and add the path to your FFmpeg bin directory, e.g., C:\FFmpeg\bin.

- Click 'OK' to close all dialog boxes.

#### On macOS:

You can install `ffmpeg` using Homebrew:

```bash
brew install ffmpeg
```

#### On Linux:
For Ubuntu and other Debian-based distributions, you can install ffmpeg from the apt repository:

```bash
sudo apt update
```

```bash
sudo apt install ffmpeg
```

## Running the app
1. **Run the Flask app**: `python app.py`
2. The app will be available at `http://127.0.0.1:5000/`

## API Endpoints
1. `/process_audio` (POST): Downloads, splits, transcribes, and generates notes from the audio of a given YouTube video URL.
   - ```bash
     curl -X POST -N http://127.0.0.1:5000/process_audio -H "Content-Type: application/json" -d '{"url": "https://www.youtube.com/watch?v=YOUR_VIDEO_ID"}'
     ```

 2. `/get_notes` (GET): Retrieves the generated notes.
    - ```bash
      curl http://127.0.0.1:5000/get_notes
      ```

