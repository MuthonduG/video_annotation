from pydub import AudioSegment
import speech_recognition as sr

def process_video(file_path):
    try:
        # Convert Video to Audio
        video = AudioSegment.from_file(file_path)
        audio = video.set_channels(1).set_frame_rate(16000).set_sample_width(2).normalize()

        # Export audio as WAV
        wav_path = file_path.rsplit(".", 1)[0] + ".wav"
        audio.export(wav_path, format="wav")

        # Transcribe Audio
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio_data = recognizer.record(source)

        # Convert Speech to Text
        transcript = recognizer.recognize_google(audio_data, language="en-US")
        return transcript
    except Exception as e:
        return f"Error processing file: {str(e)}"
