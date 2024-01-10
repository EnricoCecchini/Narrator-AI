from flask import session

def play_audio():

    while 'isPlaying' in session and session["isPlaying"]:
        print("Playing audio")