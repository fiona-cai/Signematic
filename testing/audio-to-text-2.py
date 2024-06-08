import speech_recognition as sr
from pydub import AudioSegment

def convert_audio_to_wav(audio_file_name):
    audio = AudioSegment.from_file(audio_file_name)
    wav_file_name = audio_file_name.split(".")[0] + ".wav"
    audio.export(wav_file_name, format="wav")
    return wav_file_name

def speech_to_text(audio_file_name):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file_name) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"

def main():
    audio_file_name = "audio.mp3"
    if audio_file_name.endswith(".mp3"):
        audio_file_name = convert_audio_to_wav(audio_file_name)

    text = speech_to_text(audio_file_name)
    print("Converted Text:")
    print(text)

if __name__ == "__main__":
    main()
