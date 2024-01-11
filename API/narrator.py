import os


# Narrate all lines in book
def narrate_all(lines, app, narration_data):
    print("Narrating all lines: ", lines)
    print("SPEAKER: ", narration_data["speaker"])
    print("BOOK: ", narration_data["book"])
    print("RVC MODEL: ", narration_data["rvc_model"])
    print("INDEX: ", narration_data["index"])

    audio_path = os.path.join(app.config["AUDIOBOOKS_PATH"], narration_data["book"])
    print("AUDIO PATH: ", audio_path)

    # Check if audiobook exists
    if not os.path.exists(audio_path):
        os.mkdir(audio_path)

    # Iterate lines in book
    for line in lines:

        # Check if narration is paused
        if not app.config["isNarrating"]:
            break

        # Narrate line
        narrate_line(line, narration_data, audio_path)


# Narrate single line
def narrate_line(line, narration_data, audio_path):
    print("Narrating line: ", line)

    line_index = line['path'].split('\\')[-1].replace('.txt', '')

    # save audio file
    audio_file = os.path.join(audio_path, f"{line_index}.txt")
    print("AUDIO FILE: ", audio_file)

    # Write line to audio file
    with open(audio_file, 'w', encoding='utf-8') as f:
        f.write(line['line'])


