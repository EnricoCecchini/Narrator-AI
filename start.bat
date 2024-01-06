@echo off

REM Start new CMD and run Svelte app
start cmd /k npm run dev

teimout /t 5

# REM CD into API directory and start venv in new CMD
cd API
call venv/Scripts/activate

python main.py

exit