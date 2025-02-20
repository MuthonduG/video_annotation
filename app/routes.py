import os
from flask import Blueprint, request, render_template, send_file
from werkzeug.utils import secure_filename
from .transcribe import process_video

main = Blueprint("main", __name__)

ALLOWED_EXTENSIONS = {"mp4", "avi", "mov", "mkv", "mp3", "wav"}
UPLOAD_FOLDER = "uploads"
TRANSCRIPTS_FOLDER = "transcripts"

# Function to check file extension
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Route for uploading and processing videos
@main.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Transcribe video
            transcript_text = process_video(file_path)

            # Save transcription
            transcript_filename = filename.rsplit(".", 1)[0] + ".txt"
            transcript_path = os.path.join(TRANSCRIPTS_FOLDER, transcript_filename)

            with open(transcript_path, "w", encoding="utf-8") as f:
                f.write(transcript_text)

            return f"Transcription saved! <a href='/download/{transcript_filename}'>Download</a>"

    return render_template("index.html")

# Route to download transcription
@main.route("/download/<filename>")
def download_file(filename):
    transcript_path = os.path.join(TRANSCRIPTS_FOLDER, filename)
    return send_file(transcript_path, as_attachment=True)
