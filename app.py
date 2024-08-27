import shutil
from dotenv import load_dotenv
import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import os
import time
from AudioProcessing import AudioProcessing
from NotesMaker import NotesMaker


# Load environment variables from .env file
load_dotenv(dotenv_path=os.path.join('.env'))

app = Flask(__name__)
CORS(app)  

# Initialize classes
audio_processor = AudioProcessing()
notes_maker = NotesMaker()

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_pdf(notes, output_filename="notes.pdf"):
    # Create a PDF document with letter-sized pages
    pdf = SimpleDocTemplate(output_filename, pagesize=letter)

    # Define styles for the PDF
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    title_style = ParagraphStyle(
        'Title',
        fontSize=18,
        leading=22,
        spaceAfter=14,
        alignment=1,  # Center alignment
    )

    # Content list to add paragraphs
    content = []

    # Add a title to the PDF
    title = Paragraph("Generated Notes", title_style)
    content.append(title)
    content.append(Spacer(1, 12))  # Add some space after the title

    # Split notes into paragraphs
    paragraphs = notes.split('\n')
    
    # Add each paragraph to the PDF
    for paragraph in paragraphs:
        p = Paragraph(paragraph, normal_style)
        content.append(p)
        content.append(Spacer(1, 12))  # Add some space between paragraphs

    # Build the PDF
    pdf.build(content)

    print(f"PDF generated successfully: {output_filename}")

# SSE generator to stream status updates
def stream_status(messages):
    for message in messages:
        yield f"data: {message}\n\n"
        time.sleep(1)  # Simulate processing time

@app.route('/process_audio', methods=['POST'])
def process_audio():
    if os.path.exists("notes.txt"):
        os.remove("notes.txt")
    try:
        data = request.json
        url = data.get('url')
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        # Initialize status messages
        status_messages = []

        # Step 1: Download the audio
        status_messages.append("Downloading audio...")
        audio_file_path = audio_processor.download_audio(url)
        status_messages.append("Audio downloaded.")

        # Step 2: Split the audio into smaller chunks
        status_messages.append("Splitting audio into chunks...")
        chunks = audio_processor.split_audio(audio_file_path)
        chunk_files = audio_processor.save_chunks(chunks, "audio_chunk")
        status_messages.append(f"Audio split into {len(chunk_files)} chunks.")

        # Step 3: Transcribe each chunk and write to file
        status_messages.append("Transcribing audio chunks...")
        full_transcription = ""
        for i, chunk_file in enumerate(chunk_files):
            transcription = audio_processor.transcribe(chunk_file)
            full_transcription += transcription
            status_messages.append(f"Transcribed chunk {i+1}/{len(chunk_files)}.")
        
        status_messages.append("Generating notes from transcription...")
        
        # Step 4: Generate notes from the transcribed text
        notes_maker.generate_notes(full_transcription)
        shutil.rmtree("audios")
        status_messages.append("Notes generated successfully.")

        # Return final response
        return Response(stream_status(status_messages), content_type='text/event-stream')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_notes', methods=['GET'])
def get_notes():
    try:
        with open("notes.txt", "r") as file:
            notes = file.read()
        return jsonify({"notes": notes}), 200
    except FileNotFoundError:
        return jsonify({"error": "Notes file not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
