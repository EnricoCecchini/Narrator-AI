# Narrator AI

Svelte app to generate audiobooks locally using XTTS

## Installation
1. Install Python 3.10+

2. Download `hubert_base.pt` and `rmvpe.pt` from Huggingface and place in API dir

3. Download and place `ffmpeg.exe` in API dir

3. Run start.bat


## Todo
- [x] Implement TTS
- [x] Save audios in audiobooks\BOOK
- [x] Combine audios in audiobooks\BOOK\AUDIOBOOK
- [x] Add\Delete lines in UI (And generated audio for selected line)
- [x] Reorder lines in UI
- [x] Undo unsaved changes
- [x] Save BOOK file with modified lines (Join all lines in single txt)
- [x] Save modified lines (Delete lines in books\BOOK and split new book)
- [x] Sync delete/modify audios and lines
- [x] Play audio in Svelte UI
- [x] Re-narrate selected line

## Future Plans
- [x] Implement RVC
- [ ] Implement multi-lang


## Known Bugs
