import streamlit as st
import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_to_wav(audio_file):
    audio = AudioSegment.from_file(audio_file)
    wav_file = audio_file.name.split(".")[0] + ".wav"
    audio.export(wav_file, format="wav")
    return wav_file

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"

def main():
    uploaded_file = "audio.mp3"
    file_details = {"Filename": "audio", "FileType": "mp3"}
    print(file_details)

    uploaded_file = convert_audio_to_wav(uploaded_file)

    text = speech_to_text(uploaded_file)
    print("Converted Text:")
    print(text)

if __name__ == "__main__":
    main()