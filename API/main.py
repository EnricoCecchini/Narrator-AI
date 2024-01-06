from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

from load_files import load_speakers, load_books, load_audiobooks, load_rvc_models, load_selected_book
from save_files import save_book, save_speaker

load_dotenv()

app = Flask(__name__)
CORS(app)

# app config
app.secret_key = "tts"
app.config["BOOKS_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'books')
app.config["SPEAKERS_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'speakers')
app.config["AUDIOBOOKS_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'audiobooks')
app.config["RVC_PATH"] = os.path.join(os.getenv("STATIC_PATH"), 'rvc_models')


# Load existing data

# load available books, speakers, and RVC models
@app.route("/load_existing_items", methods=["GET"])
def load_existing_items():
    speakers = load_speakers(app.config["SPEAKERS_PATH"])
    books = load_books(app.config["BOOKS_PATH"])
    audiobooks = load_audiobooks(app.config["AUDIOBOOKS_PATH"])
    rvc_models = load_rvc_models(app.config["RVC_PATH"])

    resp = jsonify({
        "speakers": speakers,
        "books": books,
        "audiobooks": audiobooks,
        "rvc_models": rvc_models
    })

    print(resp)

    return resp

@app.route("/upload_file", methods=["POST", "GET"])
def upload_file():
    if request.method == "POST":
        try:
            # Recieve new book from API
            #print(request.files['upload_book'].filename)
            if 'upload_file' in request.files:
                print(request.files['upload_file'])
                if '.txt' in request.files['upload_file'].filename:
                    resp = save_book(app.config["BOOKS_PATH"], request.files['upload_file'])
                elif '.wav' in request.files['upload_file'].filename:
                    print('SPEAKER')
                    resp = save_speaker(app.config["SPEAKERS_PATH"], request.files['upload_file'])
                else:
                    print('RVC')
                # resp = save_book(app.config["BOOKS_PATH"], request.files['upload_book'])
        except:
            return jsonify({'message': 'No Book', 'success': False})

    return resp


# Load selected book
@app.route('/load_selected_book', methods=['GET'])
def load_selected():
    selected_book = request.args.get('selected_book')

    print(selected_book)
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
def narrate_line():
    if request.method == "POST":
        data = request.get_json()

        print("NARRATE LINE: ", data)

        speaker = data["speaker"]
        book = data["book"]
        line = data["line"]
        rvc_model = data["rvc_model"]
        output_file = data["output_file"]


# Narrate entire book
@app.route("/narrate_entire_audiobook", methods=["POST", "GET"])
def narrate_entire_audiobook():
    if request.method == "POST":
        data = request.get_json()

        print("NARRATE BOOK: ", data)

        speaker = data["speaker"]
        book = data["book"]
        rvc_model = data["rvc_model"]
        output_file = data["output_file"]

# Run app
if __name__ == "__main__":
    app.run(debug=True)
