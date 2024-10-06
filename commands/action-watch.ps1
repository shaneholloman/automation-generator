Remove-Item src/logs/input_log.csv -ErrorAction Ignore
New-Item -ItemType File -Path src/logs/input_log.csv | Out-Null
Write-Output 'Watching actions...'
Write-Output 'Press ESC + mouse click to stop'
python src/action_watch.py
Write-Output 'Automation stored successfully'