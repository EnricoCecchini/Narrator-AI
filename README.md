# Narrator AI

Svelte app to generate audiobooks locally using XTTS

## Installation
1. Install Python 3.10+

2. Download `hubert_base.pt` and `rmvpe.pt` from Huggingface and place in API dir

3. Download and place `ffmpeg.exe` in API dir

3. Run start.bat (Run 2 times, first time it will install npm packages, second time it will create venv, install requirements and run the app)


## How to Use
- Run `start.bat` to start application
- Upload books, speakers, RVC mdoels and indexes (RVC and index is optional)
- Press `submit` button to upload file (Only submitted file will be uploaded)
- Reload page
- Select the uploaded book and speaker from the dropdown


## Button Guide
| Button | Description | Saves Changes |
| --- | --- | --- |
| Narrate All | Begin generating audio for all lines in book | YES |
| Pause Narration | Pause generating audio for all lines in book | NO |
| Play All | Play all generated audios from beginning to end | NO |
| Pause Playing | Stop playing generated audios | NO |
| Undo Changes | Revert line order to last unsaved changes | NO |
| Save Changes | Saves changes made to book (Reorder\Add\Delete lines) | YES |
| Merge Book | Merge generated audios for all lines in single wav file | YES |
| Play Merged | Play merged audiobook | NO |
| Index Effect | Change the strength of the index (NOT IMPLEMENTED) | NO |
| Voice Pitch | Change the pitch for the generated voice (NOT IMPLEMENTED) | NO |


# Book Editing Guide
| Button | Description | Saves Changes |
| --- | --- | --- |
| Narrate Line | Generate audio only for selected line | YES |
| Play Line | Play audio only for selected line | NO |
| Add Line Below | Add blank line below selected line | NO |
| Delete Line | Delete selected line | NO |
| Up/Down Arrows | Move selected line up/down | NO |


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
- Might have to reload the page sometimes for changes to work
