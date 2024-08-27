import os
import openai
import yt_dlp
from pydub import AudioSegment
import warnings


class AudioProcessing:
    def __init__(self, audio_dir="audios", chunk_length_ms=240000):
        self.audio_dir = audio_dir
        self.chunk_length_ms = chunk_length_ms
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

    def download_audio(self, url, output_filename="audio.mp3"):
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': os.path.join(self.audio_dir, 'audio'),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        return os.path.join(self.audio_dir, output_filename)

    def transcribe(self, audio_file_path):
        warnings.filterwarnings("ignore", category=UserWarning, message="FP16 is not supported on CPU; using FP32 instead")
        with open(audio_file_path, "rb") as audio:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio,
                response_format="text",
                language='en'
            )
        return transcription

    def split_audio(self, input_path):
        audio = AudioSegment.from_file(input_path)
        chunks = [audio[i:i+self.chunk_length_ms] for i in range(0, len(audio), self.chunk_length_ms)]
        print(f'Audio split into {len(chunks)} chunks')
        return chunks

    def save_chunks(self, chunks, base_filename):
        chunk_files = []
        for i, chunk in enumerate(chunks):
            chunk_filename = os.path.join(self.audio_dir, f"{base_filename}_part{i}.mp3")
            chunk.export(chunk_filename, format="mp3")
            chunk_files.append(chunk_filename)
        return chunk_files