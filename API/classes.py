import torch
from TTS.api import TTS
import os

class Narrator:
    def __init__(self, speaker, speakers_path, rvc=None, index=None):
        self.speaker = speaker
        self.speakers_path = os.path.join(speakers_path, speaker)
        self.rvc = rvc
        self.index = index

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.tts = TTS('tts_models/multilingual/multi-dataset/xtts_v2').to(self.device)

    def narrate(self, text, language, audiobooks_path, book, line_index):
        # Narrate text
        self.tts.tts_to_file(text=text, speaker_wav=self.speakers_path, language=language, file_path=f'{audiobooks_path}/{line_index}.wav')
