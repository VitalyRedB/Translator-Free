import pyttsx3
import speech_recognition as sr
from googletrans import Translator

"""   Библиотека для определения языка текста - работает некорректно
from langdetect import detect
text = "Hello, how are you?"
language = detect(text)
print("Language:", language)
"""
start = pyttsx3.init()
global en_voice_id, ru_voice_id
en_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'
ru_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0'
def setProEn():
    start.setProperty('voice', en_voice_id)
    start.setProperty('rate', 100)
def setProRu():
    start.setProperty('voice', ru_voice_id)
    start.setProperty('rate', 200)
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Скажи что небудь, я переведу:     a когда надоест - Скажи: "Алиса Спасибо!"')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
        try:
            task = r.recognize_google(audio, language='ru-RU').lower()  # Используем Google Web Speech API
            print()
            print(task)
            translated_text = translate_text(task)
            setProRu()
            start.say(task)
            print(translated_text)
            print()
            setProEn()
            start.say(translated_text)
            start.runAndWait()
        except sr.UnknownValueError:
            print("Я не смогла распознать речь, повтори еще раз")
            start.say("Я не смогла распознать речь")
            start.runAndWait()
            task = listen()
        except sr.RequestError as e:
            print(f"Ошибка при запросе: {e}")
            task = listen()
        return task

def answer(text):
    setProRu()
    start.say(text)
    start.runAndWait()
    global running
    running = False
    return

def requst(task):
    if "алиса спасибо" in task:
        text = "Всего наилучшего. До новых встреч!"
        answer(text)
def translate_text(text):
    translator = Translator()
    translation = translator.translate(text, src='ru', dest='en')
    return translation.text

answer("Меня завут Алиса, я безоплатный переводчик. Проверьте мой доступ к микрофону.")
print('\n Как правильно настроить микрофон на Windows 10? Выберите Пуск. Параметры. Конфиденциальность. Микрофон.\n'
      ' В области Разрешить доступ к микрофону на этом устройстве выберите Изменить и убедитесь,\n'
      ' что параметр Доступ к микрофону для этого устройства включен.\n'
      ' Затем разрешите приложениям доступ к микрофону.\n')
running = True
while running:
    requst(listen())
start.runAndWait()