from vosk import Model, KaldiRecognizer
import speech_recognition
import wave
import json
import os


def record_and_recognize_audio(*args: tuple):
    """

    """
    with microphone:
        recognized_data = ""

        #
        recognizer.adjust_for_ambient_noise(microphone, duration=2)

        try:
            print("Escuchando...")
            audio = recognizer.listen(microphone, 5, 5)

            with open("microphone-results.wav", "wb") as file:
                file.write(audio.get_wav_data())

        except speech_recognition.WaitTimeoutError:
            print("Por favor, verifique que el micrófono esté encendido?")
            return

        #  online-  Google
        try:
            print("Comenzando reconocimiento...")
            recognized_data = recognizer.recognize_google(
                audio, language="es").lower()

        except speech_recognition.UnknownValueError:
            pass

        #
        #  offline-  Vosk
        except speech_recognition.RequestError:
            print("Tratando de usar reconocimiento offline...")
            recognized_data = use_offline_recognition()

        return recognized_data


def use_offline_recognition():
    """
      - 
    :return:  
    """
    recognized_data = ""
    try:
        #
        if not os.path.exists("models/vosk-model-small-ru-0.4"):
            print("Please download the model from:\n"
                  "https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
            exit(1)

        #      (   )
        wave_audio_file = wave.open("microphone-results.wav", "rb")
        model = Model("models/vosk-model-small-ru-0.4")
        offline_recognizer = KaldiRecognizer(
            model, wave_audio_file.getframerate())

        data = wave_audio_file.readframes(wave_audio_file.getnframes())
        if len(data) > 0:
            if offline_recognizer.AcceptWaveform(data):
                recognized_data = offline_recognizer.Result()

                #      JSON-
                # (      )
                recognized_data = json.loads(recognized_data)
                recognized_data = recognized_data["text"]
    except:
        print("Sorry, speech service is unavailable. Try again later")

    return recognized_data


if __name__ == "__main__":

    #
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()

    while True:
        #
        #
        voice_input = record_and_recognize_audio()
        os.remove("microphone-results.wav")
        print(voice_input)
