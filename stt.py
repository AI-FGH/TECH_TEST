import os
import speech_recognition as sr
import argparse


def recognize_from_audio_file(audio_file_path, language="fa-IR"):
    """
    Recognizes speech from an audio file using Google Speech Recognition.

    Parameters:
    - audio_file_path: Path to the audio (.wav) file.
    - language: Language code (default is Persian 'fa-IR').
    """
    r = sr.Recognizer()

    if os.path.exists(audio_file_path):
        with sr.AudioFile(audio_file_path) as source:
            audio = r.record(source)  # Read the entire audio file
        return r.recognize_google(audio, language=language)
    else:
        raise FileNotFoundError(f"The audio file {audio_file_path} does not exist.")


def recognize_from_microphone(language="fa-IR"):
    """
    Recognizes speech from the microphone using Google Speech Recognition.

    Parameters:
    - language: Language code (default is Persian 'fa-IR').
    """
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("Microphone is active. Please say something:")
        audio = r.listen(source)

    return r.recognize_google(audio, language=language)


def main(audio_file=None, language="fa-IR"):
    """
    Main function to handle command-line inputs and perform speech recognition.
    """
    try:
        if audio_file:
            # Try to recognize from the provided audio file

            print(f"Recognized speech from file: {recognize_from_audio_file(audio_file, language)}")
            return recognize_from_audio_file(audio_file, language)
        else:
            # Fallback to microphone if no file is provided
            print(f"Recognized speech from microphone: {recognize_from_microphone(language)}")
            return recognize_from_microphone(language)

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
    except FileNotFoundError as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Speech recognition using Google API.")
    parser.add_argument('--audio_file', type=str, help='Path to the audio (.wav) file.')
    parser.add_argument('--language', type=str, default='fa-IR', help='Language for recognition (default: fa-IR).')
    args = parser.parse_args()

    main(audio_file=args.audio_file, language=args.language)
