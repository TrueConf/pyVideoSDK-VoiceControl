# Voice control of VideoSDK  with pyVideoSDK

This script implements the following features:

1. Authorization on the server.
1. Voice control.
1. Automatic transfer of a slideshow window to the second screen.

*Switch to other languages: [Russian](README_RU.md)*

## Deployment

### VideoSDK installation

VideoSDK can be downloaded [here](https://github.com/TrueConf/pyVideoSDK/blob/main/download.md). VideoSDK installation does not differ from the installation of any typical program, e.g., Notepad++.

### Installing dependencies

Installation of dependencies differs on Windows and Linux.

#### Windows

1. Install git and python3.
1. Install Poetry with PowerShell

    ```powershell
    (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
    ```

    >**NOTE**: If you have installed Python from the Microsoft Store, replace `py` with `python` in the command described above.

#### Linux

1. Run this terminal command to update current packages and install new ones:

    ```bash
    sudo apt update
    sudo apt upgrade
    sudo apt install curl git python3 python3-pip python3-dev python3-distutils festvox-ru festival-dev libportaudio2  
    sudo curl -sSL https://install.python-poetry.org | python3 -
    ```

1. Restart your computer after installation.

### Cloning and initializing the project

1. Go to the folder where the project will be saved, open the terminal and run this command:

    ```bash
    git clone --recurse-submodules https://github.com/TrueConf/pyVideoSDK-VoiceControl.git
    ```

    This command will download the repository and automatically initialize and update every sub-module in the repository.

1. Follow this [link](https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip) to download the English-language model; then, unpack it to the root of the project in the `models` folder. Other models will be available via this [link](https://alphacephei.com/vosk/models).

1. Open the terminal in the project folder and run:

    ```bash
    poetry install
    ```

    Poetry will create a virtual environment in `{project-path}/.venv/` and install Python dependencies in it.

## Settings configuration

The configuration file `config.py` includes the settings for connections, authorization and command phrases.

## Connection settings

Edit the file following the example below:  

```python
# Connection settings
IP: str = "192.168.1.2" # VideoSDK IP-address
PORT: int = 88 # Port used
PIN: str = "123" # The PIN will be used when starting VideoSDK
DEBUG = False # Write more debug information to the console and to the log-file
```

### Authorization settings

Edit the file following the example below:

```python
# Authorization settings
# IP or DNS TrueConf Server
TRUECONF_SERVER: str = "connect.trueconf.com"
# TrueConf ID of administrator, operator or user
TRUECONF_ID: str = "user01"
# Password of administrator, operator or user
PASSWORD: str = "user01"
```

If you do not have the authorization information, you can get them [here](#data-needed-for-authorization-on-the-test-server).

### Setting up the path to the folder with VOSK models

If you are not storing models in the default folder, specify the new path in the environment variable to make sure that the script works correctly:

```python
#Path to VOSK models. Default folder "models"
os.environ["VOSK_MODEL_PATH"] = 'new-path-to-folder-with-models-vosk'
```

### Language settings

In the LANG constant, specify the language that you want to use:

```python
# Language settings (in lower case)
LANG = "ru" 
```

>**NOTE:** If your language is not English, you will need to add new strings to NUMERIC and SAY constants.

### Voice settings (available only for Windows)

You can also select the voice to be used in the script:

```python
# For EN: DAVID (man), ZIRA (woman)
# For RU: IRINA (woman) 
VOICE_NAME = "IRINA"
```

### Command phrases

You can use your own command phrases in the script. To do it, edit the `HOTWORDS` dictionary in the `config.py` folder. The dictionary has the following structure:

```python
HOTWORDS = {
    'call': ('call',),
    'hello': ('Hey room',)
}
```

#### Activation of voice commands

Replace the value in the  `hello` key  with your own value. For example, if you want the script to respond to the phrase `Hi, app`, you can write (without a comma):

```python
"hello": ('Hi app')
```

In this way, you can set any activation phrase. To use multiple activation phrases, you can list them separated by commas:

```python
"hello": ('Hey room','Hi app')
```

#### Calling a user

The call will start if the script recognizes any word from the `call` list. For example, if you want the script to respond to the word `call` or any other words that you select, just add them to the list separated by commas (words should be put in quotation marks):

```python
'call': ('call', 'make call to')
```

## Start

1. Run VideoSDK with the [`--pin` parameter](https://docs.trueconf.com/videosdk/en/introduction/commandline#pin) that has the value specified in the configuration file.

    **Windows:**

    ```bash
    "C:\Program Files\TrueConf\VideoSDK\VideoSDK.exe" --pin 123
    ```

    **Linux:**

    ```bash
    trueconf-video-sdk --pin 123
    ```

1. Run the `main.py` file with Poetry:

    ```bash
    poetry run python main.py
    ```

## Use cases

The phrase `Hi room` activates voice control. Currently, it is possible to call a user with the `Call` command. However, you can [edit](#command-phrases) this list by adding your own phrases.

To activate voice recognition, say `Hi room`. You will hear a sound indicating that voice commands can now be given. Right after the sound signal, say `Call {display name}`. The display name may include text, digits and emojis. When the command is given, voice recognition is disabled until the phrase `Hi room` is spoken again.

### Example of a correct call

* James Wolf — `Call James Wolf`
* Paul Robinson 3 — `Call Paul Robinson three`
* 123-456 — `Call one two three four five six` (recommended option) or `Call one hundred and twenty-three four hundred and fifty-six` (may lead to inaccurate recognition).

If the display name includes emojis, you do not have to pronounce them separately.  

## Data needed for authorization on the test server

Go to the Telegram bot [@TrueConfSDKPromoBot](https://t.me/TrueConfSDKPromoBot) to get the server address, login, and password.
