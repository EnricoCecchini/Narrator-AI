import os
from rich import print
from rvc_infer import rvc_convert


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
            narrate_line(line, narration_data, app.config["AUDIOBOOKS_PATH"], app.config["RVC_PATH"], app.config["INDEX_PATH"], narrator)

    return {
        "message": message,
        "success": True
    }


# Narrate single line
def narrate_line(line, narration_data, AUDIOBOOKS_PATH, RVC_PATH, INDEX_PATH, narrator):
    audio_path = os.path.join(AUDIOBOOKS_PATH, narration_data["book"])
    print("Audio path: ", audio_path)
    print("Narration DATA: ", narration_data)

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

    #try:
    narrator.narrate(
        text=line['line'],
        language='en',
        audiobooks_path=audio_path,
        book=narration_data["book"],
        line_index=line_index
    )

    if narration_data["rvc_model"] == "" or narration_data["rvc_index"] == "":
        return {
            "message": "Line narrated succesfully, without RVC. Please select RVC model and index",
            "success": True
        }

    # Convert to RVC
    rvc_path = os.path.join(RVC_PATH, narration_data["rvc_model"])
    rvc_index_path = os.path.join(INDEX_PATH, narration_data["rvc_index"])

    print("RVC PATH: ", rvc_path)
    print("RVC INDEX PATH: ", rvc_index_path)

    new_audio = os.path.join(audio_path, f'{line_index}.wav').replace('/', '\\').replace('\\', '\\\\')
    print("CURRENT AUDIO PATH: ", new_audio)

    rvc_convert(
        model_path=rvc_path,
        file_index=rvc_index_path,
        input_path=new_audio,
    )

    # Delete old audio
    os.remove(new_audio)

    output_path = "./output/out.wav"
    # Move to audiobook dir
    os.rename(output_path, new_audio)

    # Delete output dir
    os.rmdir("./output")


    # rvc_convert(
    #     model_path=rvc_path,
    #     file_index=rvc_index_path,
    #     input_path=audio_path,
    #     output_dir_path=audio_path
    # )

    # os.remove(new_audio)
    # os.rename(output_path, new_audio)

    # except Exception as e:
    #     print("ERROR: ", e)
    #     return {
    #         "message": "Error narrating line",
    #         "success": False
    #     }

    return {
        "message": "Line narrated succesfully",
        "success": True
    }
