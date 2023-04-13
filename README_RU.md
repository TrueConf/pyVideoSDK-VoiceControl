# Голосовое управление VideoSDK с помощью pyVideoSDK

*Читать описание на других языках: [English](README.md)*

В данном скрипте реализованы следующие возможности:

1. Авторизация на сервере.

1. Голосовое управление.

1. Автоматический перенос раскладки презентации на второй монитор.

Подробное описание данных кейсов смотрите в статье на Хабр: [https://habr.com/ru/articles/710524/](https://habr.com/ru/articles/710524/)

Документация по TrueConf VideoSDK API / TrueConf Room API: [https://docs.trueconf.com/videosdk/introduction/common](https://docs.trueconf.com/videosdk/introduction/common)

**Другие проекты с VideoSDK:**

* [pyVideoSDK](https://github.com/zoboff/pyVideoSDK), библиотека на Python для TrueConf VideoSDK API / TrueConf Room API
* [CallButton](https://github.com/TrueConf/CallButton), пример плавающей кнопки для вызова абонента
* [pyVideoSDK-Demo](https://github.com/TrueConf/pyVideoSDK-Demo), примеры использования библиотеки pyVideoSDK
* [videosdk](https://github.com/TrueConf/videosdk), C++ библиотека для TrueConf VideoSDK API / TrueConf Room API
* [DemoQtVideoSDK](https://github.com/TrueConf/DemoQtVideoSDK), пример использования на C++ (Qt) библиотеки videosdk

## Развертывание

### Установка VideoSDK

Скачать VideoSDK можно [здесь](https://github.com/TrueConf/pyVideoSDK/blob/main/download.md). Установка VideoSDK ничем не отличается от установки обычной программы, например, Notepad++.

### Установка зависимостей

Установка зависимостей на Windows и Linux отличается.

#### Windows

1. Установите [git](https://git-scm.com/), [python3](https://www.python.org/).

1. Установите Poetry с помощью PowerShell:

```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```
>**ВНИМАНИЕ:** Если у вас установлен Python через Microsoft Store, замените `py` на `python` в приведенной выше команде.

#### Linux

1. C помощью терминала обновите текущие и установите ряд новых пакетов:

```sh
sudo apt update
sudo apt upgrade
sudo apt install curl git python3 python3-pip python3-dev python3-distutils festvox-ru festival-dev libportaudio2
sudo curl -sSL https://install.python-poetry.org | python3 -
```

2. После установки пакетов перезагрузите ваш компьютер.

### Клонирование и инициализация проекта

1. Перейдите в папку, в которой будет храниться проект, откройте терминал и выполните:

```sh
git clone --recurse-submodules https://github.com/TrueConf/pyVideoSDK-VoiceControl.git
```

Эта команда скачает репозиторий и автоматически инициализирует и обновит в нем каждый подмодуль.

2. Скачайте по данной [ссылке](https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip) архив русскоязычной модели и распакуйте его в корень проекта в папку `models`. Остальные модели доступны по [ссылке](https://alphacephei.com/vosk/models).

3. В терминале в папке с проектом выполните:

```sh
poetry install
```

Poetry создаст виртуальную среду в `{project-path}/.venv/` и установит в нее зависимости python.

## Конфигурация настроек

Файл конфигурации `config.py` содержит настройки: подключения, авторизации и командных фраз.

### Настройка подключения

Отредактируйте файл по примеру ниже:

```python
# Connection settings
IP: str = "192.168.1.2" # VideoSDK IP-address
PORT: int = 88 # Port used
PIN: str = "123" # The PIN will be used when starting VideoSDK
DEBUG = False # Write more debug information to the console and to the log-file
```

### Настройка авторизации

Отредактируйте файл по примеру ниже:

```python
# Authorization settings
# IP or DNS TrueConf Server
TRUECONF_SERVER: str = "connect.trueconf.com"
# TrueConf ID of administrator, operator or user
TRUECONF_ID: str = "user01"
# Password of administrator, operator or user
PASSWORD: str = "user01"
```

Если у вас нет данных авторизации, вы их можете получить [здесь](#данные-для-авторизации-на-тестовом-сервере).

### Настройка пути к папке с моделями VOSK

Если вы храните модели в папке не по умолчанию, то для работы скрипта укажите новый путь в переменной окружения:

```sh
#Path to VOSK models. Default folder "models"
os.environ["VOSK_MODEL_PATH"] = 'new-path-to-folder-with-models-vosk'
```

### Настройка языка

В константе LANG укажите, какой язык вы используете:

```sh
# Language settings (in lower case)
LANG = "ru"
```

**ВНИМАНИЕ:** Если ваш язык не английский и не русский, то вам нужно добавить новые строки в константы `NUMERIC` и `SAY`.

### Настройка голоса (только для Windows)

Вы можете выбрать, какой голос должен использоваться в работе скрипта:

```sh
# For EN: DAVID (man), ZIRA (woman)
# For RU: IRINA (woman) 
VOICE_NAME = "IRINA"
```

### Командные фразы

Вы можете использовать свои командные фразы в работе скрипта. Для этого отредактируйте словарь `HOTWORDS` в файлe `config.py`. Словарь имеет следующую структуру:

```python
HOTWORDS = {
    'call': ('набери', 'позвони'),
    'hello': ('привет зал')
}
```

#### Включение голосового ввода

Отредактируйте значение `hello` на свое. Например, если вы хотите, чтобы скрипт срабатывал на фразу `Приветствую, кодек` напишите (без запятых):

```python
"hello": ('приветствую кодек')
```

Таким образом вы можете задать любую фразу для активации. Для использования нескольких фраз-активаторов перечислите их через запятую:

```python
"hello": ('привет зал','приветствую кодек')
```

#### Вызов абонента

Вызов абонента происходит, если скрипт распознал любое слово из списка `call`. Например, если вы хотите, чтобы скрипт срабатывал на слова `звонок` или `вызов` добавьте их в кавычках через запятую:

```python
'call': ('набери', 'позвони', 'звонок', 'вызов')
```

## Запуск

1. Запустите VideoSDK с [параметром `--pin`](https://docs.trueconf.com/videosdk/introduction/commandline#pin) со значением указанным ранее в файле конфигурации:

**Windows:**

```sh
"C:\Program Files\TrueConf\VideoSDK\VideoSDK.exe" --pin 123
```

**Linux:**

```sh
trueconf-video-sdk --pin 123
```

2. Запустите файл `main.py` в терминале с помощью Poetry:

```sh
poetry run python main.py
```

## Использование

Фраза `Привет зал` активирует голосовой ввод команд. На данный момент доступен вызов абонента по команде `Набери` и `Позвони`, но вы можете [отредактировать](#командные-фразы) этот список, добавив свои фразы.

Для того, чтобы активировать распознавание голосовых команд скажите `Привет зал`. Вы услышите характерный звук, обозначающий доступность ввода команды. Сразу после звукового сигнала скажите `Набери {отображаемое имя}`. Отображаемое имя может содержать: текст, цифры, эмоджи. После произнесения команды распознавание прекращается до повтора фразы `Привет зал`.

### Пример правильного вызова

* Иван Иванов — `Набери Иван Иванов`;

* Сергей Петров 3 — `Набери Сергей Петров три`;

* 123-456 — `Набери один два три четыре пять шесть` (рекомендованный способ) или `Набери сто двадцать три четыреста пятьдесят шесть` (могут возникать неточности);

Если в отображаемом имени есть эмоджи, их проговаривать не нужно.

## Данные для авторизации на тестовом сервере

Перейдите в Telegram бота [@TrueConfSDKPromoBot](https://t.me/TrueConfSDKPromoBot) для получения данных: сервер, логин и пароль.
