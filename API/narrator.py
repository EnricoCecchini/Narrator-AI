import os
from rich import print


# Narrate all lines in book
def narrate_all(lines, app, narration_data, narrator):
    audio_path = os.path.join(app.config["AUDIOBOOKS_PATH"], narration_data["book"])

    message = ""

    # Check if audiobook exists
    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    # Iterate lines in book
    for line in lines:

        print('NARRATING: ', app.config["isNarrating"])
        # Check if narration is paused
        if not app.config["isNarrating"]:
            message = "Narration paused"
            print(message)
            break

        # Narrate line
        if line['line'] != "":
            narrate_line(line, narration_data, app.config["AUDIOBOOKS_PATH"], narrator)

    return {
        "message": message,
        "success": True
    }


# Narrate single line
def narrate_line(line, narration_data, AUDIOBOOKS_PATH, narrator):
    audio_path = os.path.join(AUDIOBOOKS_PATH, narration_data["book"])
    print("Audio path: ", audio_path)

    # Check if audiobook exists
    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    print("Narrating line: ", line)
    line_index = line['path'].split('\\')[-1].replace('.txt', '')

    if line['line'] == "":
        return {
            "message": "Empty line",
            "success": False
        }

    try:
        narrator.narrate(
            text=line['line'],
            language='en',
            audiobooks_path=audio_path,
            book=narration_data["book"],
            line_index=line_index
        )

    except Exception as e:
        print("ERROR: ", e)
        return {
            "message": "Error narrating line",
            "success": False
        }

    return {
        "message": "Line narrated succesfully",
        "success": True
    }
