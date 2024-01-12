@echo off

REM Install npm packages if not already installed
if not exist node_modules (
    npm install
) else (
    echo "node_modules already exists"
)

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

    pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

    pip install -e git+https://github.com/JarodMica/rvc.git#egg=rvc

    pip install -e git+https://github.com/JarodMica/rvc-tts-pipeline.git#egg=rvc_tts_pipe

) else (
    echo "venv already exists"

    REM activate venv
    call venv/Scripts/activate
)

REM Run API
python main.py

exit