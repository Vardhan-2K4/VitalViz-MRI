@echo off
echo Starting Flask Backend...
start cmd /k "cd src && python app_server.py"

timeout /t 3 /nobreak >nul

echo Starting React Frontend...
start cmd /k "npm start"

exit
