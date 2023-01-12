"""Settings and constant file"""

import os

import sounddevice as sd
import soundfile as sf

# Connection settings
IP: str = "10.10.10.10"  # VideoSDK IP-address
PORT: int = 88  # Port used
PIN: str = "123"  # The PIN will be used when starting VideoSDK
DEBUG = False  # Write more debug information to the console and to the log-file


# Authorization settings
# IP or DNS TrueConf Server
TRUECONF_SERVER: str = "connect.trueconf.com"

# TrueConf ID of administrator, operator or user
TRUECONF_ID: str = "user01"

# Password of administrator, operator or user
PASSWORD: str = "user01"

# Command phrase settings
HOTWORDS = {
    'ru': {
        # this must be tuple and only lower case
        'call': ('набери', 'позвони',),
        # this must be tuple
        'hello': ('Привет зал',)
    },
    'en': {
        # this must be tuple and only lower case
        'call': ('call', 'make call to'),
        # this must be tuple
        'hello': ('Hey room',)
    }
}

#Path to VOSK models. Default folder "models"
os.environ["VOSK_MODEL_PATH"] = 'models'

# Similarity percentage 0..1
SIMILARITY_PERCENTAGE: float = 0.85

# Language settings (in lower case)
# For English enter 'en' and for Russian enter 'ru'
LANG = "ru"

# Voices settings (only for Windows)
# For EN: DAVID (man), ZIRA (woman)
# For RU: IRINA (woman)
VOICE_NAME = "IRINA"

# Dict for convert text numbers to int type
NUMERIC = {
    "ru": {
        'ноль': 0, 'один': 1,  'два': 2,  'три': 3,
        'четыре': 4,  'пять': 5,  'шесть': 6,
        'семь': 7,  'восемь': 8,  'девять': 9,
        'десять': 10,  'одиннадцать': 11,  'двенадцать': 12,
        'тринадцать': 13,  'четырнадцать': 14,  'пятнадцать': 15,
        'шестнадцать': 16,  'семнадцать': 17,  'восемнадцать': 18,
        'девятнадцать': 19,  'двадцать': 20,  'тридцать': 30,
        'сорок': 40,  'пятьдесят': 50,  'шестьдесят': 60,
        'семьдесят': 70,  'восемьдесят': 80,  'девяносто': 90,
        'сто': 100,  'двести': 200,  'триста': 300,
        'четыреста': 400,  'пятьсот': 500,  'шестьсот': 600,
        'семьсот': 700,  'восемьсот': 800,  'девятьсот': 900
    },
    "en": {
        'zero': 0, 'one': 1,  'two': 2,  'three': 3,
        'four': 4,  'five': 5,  'six': 6,
        'seven': 7,  'eight': 8,  'nine': 9,
        'ten': 10,  'eleven': 11,  'twelve': 12,
        'thirteen': 13,  'fourteen': 14,  'fifteen': 15,
        'sixteen': 16,  'seventeen': 17,  'eighteen': 18,
        'nineteen': 19,  'twenty': 20,  'thirty': 30,
        'forty': 40,  'fifty': 50,  'sixty': 60,
        'seventy': 70,  'eighty': 80,  'ninety': 90,
        'one hundred': 100,  'two hundred': 200,  'three hundred': 300,
        'four hundred': 400,  'five hundred': 500,  'six hundred': 600,
        'seven hundred': 700,  'eight hundred': 800,  'nine hundred': 900
    }
}

# Dict with phrases for text-to-speech
SAY = {
    'ru': {
        'call': 'Набираю абонента',
        'hello': 'Скрипт запущен и готов выполнять команды',
        'not_of_found': 'Абонента с именем {} не найдено в адресной книге. '
        'Пожалуйста, повторите попытку.'
    },
    'en': {
        'call': 'I dial a subscriber',
        'hello': 'The script is running and ready to execute commands',
        'not_of_found': 'The subscriber with the name {} was not found in the address book. '
        'Please try again.'
    }
}


class Sounds():
    """Class for plays sounds"""
    def __init__(self) -> None:

        self.d_start, self.fs_start = sf.read(
            "sounds/start.wav", dtype='float32')
        self.d_done, self.fs_done = sf.read("sounds/done.wav", dtype='float32')
        self.d_error, self.fs_error = sf.read(
            "sounds/error.wav", dtype='float32')

    def start(self):
        """Plays the voice assistant activation sound"""
        sd.play(self.d_start, self.fs_start)
        sd.wait()

    def done(self):
        """Plays a sound if recognition is successful"""
        sd.play(self.d_done, self.fs_done)
        sd.wait()

    def error(self):
        """Plays a sound if recognition fails"""
        sd.play(self.d_error, self.fs_error)
        sd.wait()
