@echo off

REM Start new CMD and run Svelte app
start cmd /k npm run dev

REM timeout /t 5

REM CD into API directory and start venv in new CMD
cd API

REM Check if venv exists, if not create it
set VENV_DIR=venv

if not exist %VENV_DIR% (
    python -m venv venv

    call venv/Scripts/activate

    REM Install requirements
    pip install -r requirements.txt

) else (
    echo "venv already exists"

    REM activate venv
    call venv/Scripts/activate
)

REM Run API
python main.py

exit