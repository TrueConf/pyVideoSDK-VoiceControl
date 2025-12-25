#!/usr/bin/env python3

"""
Voice control for TrueConf Room using python-trueconf-room

This script implements the following features:

1. Authorization on the server.
2. Voice control.
3. Automatic transfer of a slideshow window to the second screen.
"""

import queue
import time
import sys
import os

from typing import Final

import orjson
import sounddevice as sd
import vosk
import Levenshtein

import trueconf_room
import trueconf_room.consts as C
from trueconf_room.methods import Methods
from trueconf_room.consts import EVENT, METHOD_RESPONSE
import config

if os.name == 'posix':
    import festival
else:
    import pyttsx3
    pyttsx3_engine = pyttsx3.init()
    for voice in pyttsx3_engine.getProperty('voices'):
        if config.VOICE_NAME in voice.id:
            print(f"Set voice {config.VOICE_NAME}")
            pyttsx3_engine.setProperty('voice', voice.id)

# create queue
q = queue.Queue()
# set default microphone device
device = sd.default.device
# calculate samplerate
samplerate = int(sd.query_devices(device, 'input')['default_samplerate'])
# create sounds object
sounds = config.Sounds()
# create TrueConf Room object
room = trueconf_room.open_session(ip=config.IP,
                              port=config.PORT,
                              pin=config.PIN,
                              debug=config.DEBUG)
# create methods object
methods = Methods(room)

# load vosk model based on LANG
model = vosk.Model(lang=config.LANG)


def tts_say(text: str):
    """
    Play text using TTS modules:
    Linux — festival
    Windows — pyttsx3
    """
    if os.name == 'posix':
        festival.sayText(text)
        time.sleep(1)
    else:
        pyttsx3_engine.say(text)
        pyttsx3_engine.runAndWait()
        pyttsx3_engine.stop()


def text_to_number(text_with_number: tuple):
    """This function convert text number to number"""
    numbers = config.NUMERIC[config.LANG]
    return "".join([str(numbers[i]) if i in numbers else i for i in text_with_number])


def contact_diff(response):
    """Match inbox string with strings from TrueConf Room address book (Abook parametr)"""
    match_list = {}
    for display_name in Abook:
        concat_name = ''.join(display_name.split()).lower()
        match_list[display_name] = Levenshtein.jaro_winkler(
            text_to_number(response), concat_name)
    return max(match_list.items(), key=lambda x: x[1])


def call(*args):
    """Call contact from TrueConf Room address book"""
    if args:
        name_to_call, percentage = contact_diff(*args)
        if percentage >= config.SIMILARITY_PERCENTAGE:
            tts_say(f"{config.SAY[config.LANG]['call']}{name_to_call}")
            methods.call(Abook[name_to_call])
        else:
            tts_say(config.SAY[config.LANG]['not_of_found'].format(*args))


def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def execute_command_with_name(command: str, *args: list):
    """Parse command and call it"""
    for command_names, func in COMMANDS.items():
        if command in command_names:
            sounds.done()
            func(*args)


def activation(phrase: tuple):
    """Check activation phrase"""
    if not phrase:
        return False
    else:
        if isinstance(HELLO, tuple):
            for i in HELLO:
                if i.lower() in " ".join(phrase):
                    return True
        else:
            print(f"ERROR: '{HELLO}' in HOTWORDS[lang]['hello'] must be tuple")
    return False


def main():
    """
    The main function with a loop
    in which VOSK recognizes the voice and
    sends the text for further processing
    """
    tts_say(config.SAY[config.LANG]['hello'])
    with sd.RawInputStream(samplerate=samplerate,
                           blocksize=8000,
                           device=device,
                           dtype='int16',
                           channels=1,
                           callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        try:
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    phrase = orjson.loads(rec.FinalResult())['text'].split()
                    print("Background recognition", phrase)
                    if activation(phrase):
                        sounds.start()
                        current_time = time.monotonic()
                        commands = []
                        while time.monotonic() - current_time <= 6:
                            data = q.get()
                            if rec.AcceptWaveform(data):
                                commands += orjson.loads(rec.Result()
                                                         )['text'].split()
                                print("Сommand recognition", commands)
                        if commands:
                            command = commands[0]
                            command_options = [str(input_part)
                                               for input_part in commands[1:len(commands)]]
                            execute_command_with_name(command, command_options)
                        else:
                            sounds.error()
                if not room.isConnected():
                    break
        except KeyboardInterrupt:
            print('Exit by Ctrl + c')
        except trueconf_room.CustomSDKException as exception:
            print(f'TrueConf Room error: {exception}')


@room.handler(METHOD_RESPONSE[C.M_getAbook])
def on_getAbook(response):
    """Get address book from TrueConf Room"""
    print('on_getAbook')
    global Abook
    Abook = {}
    for user in response['abook']:
        try:
            Abook[user['peerDn']] = user['peerId']
        except IndexError:
            continue


@room.handler(METHOD_RESPONSE[C.M_getMonitorsInfo])
def on_getMonitorInfo(response):
    """Found free monitor"""
    global IndexSlideshowMonitor
    for monitor in response['monitors']:
        if monitor['index'] == response['currentMonitor']:
            continue
        IndexSlideshowMonitor = monitor['index']
        break


@room.handler(EVENT[C.EV_contactsRenamed])
@room.handler(EVENT[C.EV_contactsAdded])
@room.handler(EVENT[C.EV_contactsDeleted])
def update_abook(response):
    """Func is updated address book in Abook paramater"""
    methods.getAbook()


@room.handler(EVENT[C.EV_videoMatrixChanged])
def on_moveVideoSlotToMonitor(response):
    """Func is moved video slot to other monitor (second, free monitor)"""
    methods.getMonitorsInfo()
    for i in response["participants"]:
        if '#contentSharing' in i['peerId']:
            methods.moveVideoSlotToMonitor(
                callId=i['peerId'], monitorIndex=IndexSlideshowMonitor)
            break


@room.handler(EVENT[C.EV_login])
def on_state_change(response):
    """Printed to console message about successfully authenticated to the server"""
    if response["result"] == 0:
        print(f'{response["peerDn"]} successfully authenticated to the server')
        methods.getAbook()


@room.handler(EVENT[C.EV_serverConnected])
def on_serverConnected(response):
    """Need to login"""
    methods.login(config.TRUECONF_ID, config.PASSWORD)


COMMANDS: Final = {config.HOTWORDS[config.LANG]["call"]: call}
HELLO: Final = config.HOTWORDS[config.LANG]["hello"]

if __name__ == '__main__':
    # Try to connect to TrueConf Server
    methods.connectToServer(config.TRUECONF_SERVER)
    main()
