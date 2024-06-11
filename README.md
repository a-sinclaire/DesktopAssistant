# DesktopAssistant

*a little friend for your desktop :3*

## Contents

### DesktopAssistant

Contains just the little friend, who can be controlled via system tray icon. Will always be shown unless explicitly hidden.

### SleepAssistant

A program that pops up the little friend at night time to go remind you to go to bed. When night time starts, and how long night time lasts can be set as launch options.

```
usage: SleepAssistant [-h] [-s NIGHTSTART] [-t NIGHTLENGTH]

options:
  -h, --help            show this help message and exit
  -s NIGHTSTART, --nightStart NIGHTSTART
                        Time sleep assistant will appear in format "HH:MM"
  -t NIGHTLENGTH, --nightLength NIGHTLENGTH
                        Duration sleep assistant will stay on screen in minutes
```

## Running the program

With `python-poetry`:
```
$ poetry run DesktopAssistant
$ poetry run SleepAssistant
```

The Python package containing the program can also be downloaded and installed from the DesktopAssistant GitHub release page:
```
$ pip install https://github.com/a-sinclaire/DesktopAssistant/releases/latest/download/desktopassistant-0.0.1-py3-none-any.whl [--user]
$ DesktopAssistant
$ SleepAssistant
```

## Development notes

<sub>More to come...</sub>
