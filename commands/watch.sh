#!/bin/bash

rm src/logs/input_log.csv
touch src/logs/input_log.csv
echo 'Watching actions...'
echo 'Press ESC + mouse click to stop'
python src/watch.py
echo 'Automation stored successfully'
