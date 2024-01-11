from flask import session

def play_audio(lines, app):

    while app.config["isNarrating"]:
        print("Playing audio")