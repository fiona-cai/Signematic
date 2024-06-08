import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO


def speech_to_text(audio_file_name):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_mp3(audio_file_name)
    audio_data = BytesIO()
    audio.export(audio_data, format="wav")
    audio_data.seek(0)

    with sr.AudioData(audio_data, 16000, 2) as source:
        try:
            text = recognizer.recognize_google(source)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"


def main():
    audio_file_name = "audio.mp3"
    text = speech_to_text(audio_file_name)
    print("Converted Text:")
    print(text)


if __name__ == "__main__":
    main()
