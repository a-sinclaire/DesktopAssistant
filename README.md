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

Otherwise:
```
$ pip install desktopassistant-0.0.1-py3-none-any.whl [--user]
$ DesktopAssistant
$ SleepAssistant
```
<sub>
(this is a janky temporary solution that will be fixed once this is on PyPi)
</sub>

## Development notes

If you'd like to add/remove/rename assets when tinkering with this project, you should edit the `assets/assets.qrc` file and recompile assets.py. A little utility script to do this is located in `misc/generate_assets.sh`, which will do this for you. More info can be found in [this tutorial](https://www.pythonguis.com/tutorials/packaging-data-files-pyside6-with-qresource-system/).

