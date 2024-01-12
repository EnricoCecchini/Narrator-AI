import os
import threading

from dotenv import load_dotenv
from flask import Flask, jsonify, request, session
from flask_cors import CORS
from load_files import (load_audiobooks, load_books, load_index_files,
                        load_rvc_models, load_selected_book, load_speakers)
from narrator import narrate_all, narrate_line
from play_audio import play_audio
from rich import print
from save_files import (remove_deleted_audios, reorder_audios, save_book,
                        save_index, save_rvc, save_speaker, update_book,
                        merge_audiobook)

from classes import Narrator

load_dotenv()

app = Flask(__name__)
CORS(app)

# app config
app.secret_key = "tts"
app.config["BOOKS_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'books')
app.config["SPEAKERS_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'speakers')
app.config["AUDIOBOOKS_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'audiobooks')
app.config["RVC_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'rvc_models')
app.config["INDEX_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'index')

app.config["isNarrating"] = False


# Load existing data

# load available books, speakers, and RVC models
@app.route("/load_existing_items", methods=["GET"])
def load_existing_items():
    session['isPlaying'] = False
    session["isNarrating"] = False

    speakers = load_speakers(app.config["SPEAKERS_PATH"])
    books = load_books(app.config["BOOKS_PATH"])
    audiobooks = load_audiobooks(app.config["AUDIOBOOKS_PATH"])
    rvc_models = load_rvc_models(app.config["RVC_PATH"])
    indexes = load_index_files(app.config["INDEX_PATH"])

    resp = jsonify({
        "speakers": speakers,
        "books": books,
        "audiobooks": audiobooks,
        "rvc_models": rvc_models,
        "indexes": indexes
    })

    print(resp)

    return resp

@app.route("/upload_file", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        try:
            # Recieve new book from API
            if 'upload_file' in request.files:
                print(request.files['upload_file'])
                if '.txt' in request.files['upload_file'].filename:
                    resp = save_book(app.config["BOOKS_PATH"], request.files['upload_file'])

                elif '.wav' in request.files['upload_file'].filename:
                    print('SPEAKER')
                    resp = save_speaker(app.config["SPEAKERS_PATH"], request.files['upload_file'])

                elif '.pth' in request.files['upload_file'].filename:
                    print('RVC')
                    resp = save_rvc(app.config["RVC_PATH"], request.files['upload_file'])

                elif '.index' in request.files['upload_file'].filename:
                    print('INDEX')
                    resp = save_index(app.config["INDEX_PATH"], request.files['upload_file'])

                else:
                    return jsonify({
                        'message': 'Invalid file type',
                        'success': False
                    })
        except:
            return jsonify({'message': 'No Book', 'success': False})

    return resp


# Load selected book
@app.route('/load_selected_book', methods=['GET'])
def load_selected():
    selected_book = request.args.get('selected_book')

    print('LOAD SELECTED BOOK', selected_book)
    try:
        book_content = load_selected_book(app.config["BOOKS_PATH"], selected_book)

    except Exception as e:
        return jsonify({'message': 'Error reading book', 'success': False, 'error': e, 'data': []})

    result = jsonify({'message': 'Book loaded succesfully', 'success': True, 'error': '', 'data': book_content})
    print('RESULT: ', result.get_data(as_text=True))

    return result


# Generate audio

# Narrate specific line
@app.route("/narrate_line", methods=["POST", "GET"])
def narrate_line_route():
    if request.method == "POST":
        data = request.get_json()

        print("NARRATE LINE: ", data)

        narration_data = {
            "speaker": data["speaker"],
            "book": data["book"],
            "rvc_model": data["rvc_model"],
            "index": data["index"],
            "line": data["line"]
        }

        print("line: ", narration_data["line"])

        if narration_data["speaker"] == "":
            return jsonify({
                'message': 'No Speaker',
                'success': False,
                'error': '',
                'data': []
            })

        elif narration_data["book"] == "":
            return jsonify({
                'message': 'No Book',
                'success': False,
                'error': '',
                'data': []
            })

        elif len(narration_data["line"]['line']) == 0:
            return jsonify({
                'message': 'No Line',
                'success': False,
                'error': '',
                'data': []
            })

        narrator = Narrator(
            speaker=narration_data["speaker"],
            speakers_path=app.config["SPEAKERS_PATH"],
            rvc=narration_data["rvc_model"],
            index=narration_data["index"]
        )

        # Narrate line
        narrate_line(narration_data["line"], narration_data, app.config["AUDIOBOOKS_PATH"], narrator)

    return jsonify({'message': 'Line narrated succesfully', 'success': True, 'error': '', 'data': []})


# Narrate entire book
@app.route("/narrate_entire_audiobook", methods=["POST", "GET"])
def narrate_entire_audiobook():
    if request.method == "POST":
        if app.config["isNarrating"]:
            print("Already narrating")

            return jsonify({
                'message': 'Already narrating',
                'success': False,
                'error': '',
                'data': []
            })

        app.config["isNarrating"] = True

        data = request.get_json()

        print("NARRATE BOOK: ")

        narration_data = {
            "speaker": data["speaker"],
            "book": data["book"],
            "rvc_model": data["rvc_model"],
            "index": data["index"]
        }

        if narration_data["speaker"] == "":
            return jsonify({
                'message': 'No Speaker',
                'success': False,
                'error': '',
                'data': []
            })

        elif narration_data["book"] == "":
            return jsonify({
                'message': 'No Book',
                'success': False,
                'error': '',
                'data': []
            })

        narrator = Narrator(
            speaker=narration_data["speaker"],
            speakers_path=app.config["SPEAKERS_PATH"],
            rvc=narration_data["rvc_model"],
            index=narration_data["index"]
        )

        # Load lines from book
        lines = load_selected_book(app.config["BOOKS_PATH"], narration_data["book"])

        session["narration_data"] = {
            "speaker": narration_data["speaker"],
            "book": narration_data["book"],
            "rvc_model": narration_data["rvc_model"],
            "index": narration_data["index"]
        }

        # Start narration thread
        narration_thread = threading.Thread(target=narrate_all, args=[lines, app, narration_data, narrator])
        narration_thread.start()

    return jsonify({
        'message': 'Book narrated succesfully',
        'success': True,
        'error': '',
        'data': []
    })


# Pause entire audiobook narration
@app.route("/pause_narration", methods=["POST", "GET"])
def pause_narration():
    if request.method == "POST":
        session["isNarrating"] = False

        app.config["isNarrating"] = False

        print("Narration Pauses", app.config["isNarrating"])

    return jsonify({
        'message': 'Narration paused succesfully',
        'success': True,
        'error': '',
        'data': []
    })


@app.route('/save_book_changes', methods=['POST'])
def save_book_changes():
    data = request.get_json()

    print('SAVE BOOK CHANGES: ', data)

    if data['book'] == '':
        return jsonify({
            'message': 'No Book',
            'success': False,
            'error': '',
            'data': []
        })

    elif data['lines'] == []:
        return jsonify({
            'message': 'No Lines',
            'success': False,
            'error': '',
            'data': []
        })

    remaining_lines_index = []

    for i, line in enumerate(data["lines"]):

        new_line = {
            'line': line['line'],
            'new_index': i,
            'old_index': line['path'].split('\\')[-1].replace('.txt', '')
        }
        print(i, line)

        remaining_lines_index.append(new_line)

    print('REMAINING LINES INDEX: ', remaining_lines_index)

    # Update book with updated lines
    update_book(app.config["BOOKS_PATH"], data, remaining_lines_index)

    # Delete audios for deleted lines
    remove_deleted_audios(app.config["AUDIOBOOKS_PATH"], data["book"], remaining_lines_index)

    # Reorder audios to match new line order
    reorder_audios(app.config["AUDIOBOOKS_PATH"], data["book"], remaining_lines_index)

    print('BOOK SAVED')

    return jsonify({
        'message': 'Book updates succesfully',
        'success': True,
        'error': '',
        'data': []
    })


@app.route('/check_audio_exists', methods=['GET', 'POST'])
def check_audio_exists(audio_path="Hello"):
    audio_path = request.json['audio_path']

    print('\n\nCHECKING AUDIO!!!\n')
    print('CHECK AUDIO EXISTS: ', audio_path)

    if not audio_path:
        return jsonify({
            'message': 'No audio path',
            'success': False,
            'error': '',
            'data': []
        })

    audio_path = audio_path.replace('%20', ' ')

    print('CHECK AUDIO EXISTS: ', audio_path)

    if os.path.exists(audio_path):
        return jsonify({
            'message': 'Audio exists',
            'success': True,
            'error': '',
            'data': []
        })

    else:
        return jsonify({
            'message': 'Audio does not exist',
            'success': False,
            'error': '',
            'data': []
        })


@app.route('/check_all_audios_exist', methods=['GET', 'POST'])
def check_all_audios_exist():
    data = request.get_json()

    print('CHECK ALL AUDIOS EXIST: ', data)

    if data['book'] == '':
        return jsonify({
            'message': 'No Book',
            'success': False,
            'error': '',
            'data': []
        })

    audio_path = os.path.join(app.config["AUDIOBOOKS_PATH"], data['book']['book'])
    existing_audios = os.listdir(audio_path)

    lines_path = os.path.join(app.config["BOOKS_PATH"], data['book']['book'], 'Processed')
    existing_lines = os.listdir(lines_path)

    print('EXISTING AUDIOS: ', existing_audios)
    print('EXISTING LINES: ', existing_lines)

    if len(existing_audios) != len(existing_lines):
        return jsonify({
            'message': 'Not all audios exist',
            'success': False,
            'error': '',
            'data': []
        })

    return jsonify({
        'message': 'All audios exist',
        'success': True,
        'error': '',
        'data': []
    })


@app.route('/merge_audiobook', methods=['GET', 'POST'])
def merge_book():
    data = request.get_json()

    print('MERGE BOOK: ', data)

    if data['book'] == '':
        return jsonify({
            'message': 'No Book',
            'success': False,
            'error': '',
            'data': []
        })

    elif data['lines'] == []:
        return jsonify({
            'message': 'No Lines',
            'success': False,
            'error': '',
            'data': []
        })

    merge_audiobook(app.config["AUDIOBOOKS_PATH"], data["book"], data["lines"])

    return jsonify({
        'message': 'Book merged succesfully',
        'success': True,
        'error': '',
        'data': []
    })



# Run app
if __name__ == "__main__":
    app.run(debug=True)
