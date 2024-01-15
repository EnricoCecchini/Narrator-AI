@echo off

REM Install npm packages if not already installed
if not exist node_modules (
    npm ci --quiet
) else (
    echo "node_modules already exists"
)

REM Start new CMD and run Svelte app
start cmd /k npm run dev

timeout /t 5

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

REM Check if curl is available
where curl >nul 2>nul
if %errorlevel% neq 0 (
    echo "Error: curl is not found in the system's PATH. Please install curl."
    exit /b 1
)

REM Download hubert_base.pt, rmvpe.pt, and ffmpeg.exe and store in the API directory
if not exist "hubert_base.pt" (
    echo "Downloading hubert_base.pt"
    curl -L -o "hubert_base.pt" "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/hubert_base.pt?download=true"
) else (
    echo "hubert_base.pt already exists"
)

if not exist "rmvpe.pt" (
    echo "Downloading rmvpe.pt"
    curl -L -o "rmvpe.pt" "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/rmvpe.pt?download=true"
) else (
    echo "rmvpe.pt already exists"
)

if not exist "ffmpeg.exe" (
    echo "Downloading ffmpeg.exe"
    curl -L -o "ffmpeg.exe" "https://huggingface.co/lj1995/VoiceConversionWebUI/resolve/main/ffmpeg.exe?download=true"
) else (
    echo "ffmpeg.exe already exists"
)


REM Run API
python main.py

exit