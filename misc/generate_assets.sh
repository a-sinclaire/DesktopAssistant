#!/bin/bash

if [[ -d "assets" ]]; then
    # script is being ran from repository root
    cd assets
elif [[ -f "generate_assets.sh" ]]; then
    # script is being ran from /misc
    cd ../assets
fi

if [[ -f "assets.qrc" ]]; then
    pyside6-rcc assets.qrc -o ../src/DesktopAssistant/assets.py
else
    echo "Could not locate assets.qrc in $(pwd)"
    exit 1
fi

exit 0
