import os
from rich import print
import wave


# Save book and parse into individual files for each sentence
def save_book(BOOKS_PATH, book):
    # Make path for uploaded book
    new_book_path = os.path.join(BOOKS_PATH, book.filename.replace(".txt", ""))
    processed_path = os.path.join(new_book_path, "Processed")

    # If path exists, return error
    if os.path.exists(new_book_path):
        return {"message": "Book already exists", "success": False}

    os.makedirs(new_book_path)
    os.makedirs(processed_path)

    # Save OG book
    book.save(os.path.join(new_book_path, book.filename))

    # Read book and split into lines in separate files in Processed dir
    with open(os.path.join(new_book_path, book.filename), 'r', encoding='utf-8') as file:
        lines = file.readlines()

        # Skip empty lines
        lines = [l for l in lines if len(l.replace('\n', '')) > 0]

        for i, line in enumerate(lines):
            with open(os.path.join(processed_path, f"{i}.txt"), 'w', encoding='utf-8') as f:
                f.write(line)

    return {
        "message": "Book uploaded and processed succesfully",
        "success": True
    }


# Delete audios generated for deleted lines
def remove_deleted_audios(AUDIOBOOKS_PATH, book, remaining_lines_index):
    old_indexes = [int(line["old_index"]) for line in remaining_lines_index if line["old_index"] != ""]

    print("OLD INDEXES: ", old_indexes)

    audio_files = os.listdir(os.path.join(AUDIOBOOKS_PATH, book))
    if "audiobook" in audio_files:
        audio_files.remove("audiobook")

    # Delete audios by index
    for file in audio_files:
        try:
            if int(file.replace(".wav", "")) not in old_indexes:
                print("DELETING: ", file.replace(".wav", ""))
                os.remove(os.path.join(AUDIOBOOKS_PATH, book, file))
        except FileNotFoundError:
            print("Audio does not exist")

    return {
        "message": "Audios deleted succesfully",
        "success": True
    }


# Reorder audios to match new line order
def reorder_audios(AUDIOBOOKS_PATH, book, remaining_lines_index):

    print("REORDERING AUDIOS: ", remaining_lines_index)
    print('AUDIO PATH: ', os.path.join(AUDIOBOOKS_PATH, book))

    audio_files = os.listdir(os.path.join(AUDIOBOOKS_PATH, book))
    if "audiobook" in audio_files:
        audio_files.remove("audiobook")

    print('FILES: ', audio_files)

    # Rename audios to new index
    for file in audio_files:
        try:
            for l in remaining_lines_index:
                if l["old_index"] == file.replace(".wav", ""):
                    print("RENAMING: ", os.path.join(AUDIOBOOKS_PATH, book, file), " TO: ", os.path.join(AUDIOBOOKS_PATH, book, f"{l['new_index']}-NEW.wav"))
                    os.rename(os.path.join(AUDIOBOOKS_PATH, book, file), os.path.join(AUDIOBOOKS_PATH, book, f"{l['new_index']}-NEW.wav"))
            #os.rename(os.path.join(AUDIOBOOKS_PATH, book, file), os.path.join(AUDIOBOOKS_PATH, book, f"{remaining_lines_index[int(file.replace('.wav', ''))]} -NEW.wav"))
            #os.rename(os.path.join(AUDIOBOOKS_PATH, book, file), os.path.join(AUDIOBOOKS_PATH, book, f"{remaining_lines_index[int(file.replace('.txt', ''))]} -NEW.wav"))
        except FileNotFoundError:
            pass

    # Rename audios to remove -NEW
    print('REMOVE -NEW FROM FILE NAME')

    audio_files = os.listdir(os.path.join(AUDIOBOOKS_PATH, book))

    if "audiobook" in audio_files:
        audio_files.remove("audiobook")

    for file in audio_files:
        try:
            print('REMOVE -NEW: ', os.path.join(AUDIOBOOKS_PATH, book, file), ' TO: ', os.path.join(AUDIOBOOKS_PATH, book, file.replace('-NEW', '')))
            os.rename(os.path.join(AUDIOBOOKS_PATH, book, file), os.path.join(AUDIOBOOKS_PATH, book, file.replace('-NEW', '')))
        except FileNotFoundError:
            pass

    return {
        "message": "Audios reordered succesfully",
        "success": True
    }


# Update book and parse into individual files for each sentence
def update_book(BOOKS_PATH, data, remaining_lines_index):
    update_book_path = os.path.join(BOOKS_PATH, data["book"])

    print("NEW LINE ORDER: ", remaining_lines_index)

    if not os.path.exists(update_book_path):
        return {
            "message": "Book does not exist",
            "success": False
        }

    # Delete from Processed dir
    for file in os.listdir(os.path.join(update_book_path, "Processed")):
        os.remove(os.path.join(update_book_path, "Processed", file))

    # Delete book
    os.remove(os.path.join(update_book_path, f'{data["book"]}.txt'))

    for i, line in enumerate(data["lines"]):
        with open(os.path.join(update_book_path, "Processed", f"{i}.txt"), 'w', encoding='utf-8') as f:
            f.write(line["line"])

        # Append to book
        with open(os.path.join(update_book_path, f'{data["book"]}.txt'), 'a', encoding='utf-8') as f:
            f.write(f'{line["line"]}\n')

    return {
        "message": "Book updated succesfully",
        "success": True
    }


# Save speaker in speakers dir
def save_speaker(SPEAKERS_PATH, speaker):
    new_speaker_path = os.path.join(SPEAKERS_PATH, speaker.filename)

    # If path exists, return error
    if os.path.exists(new_speaker_path):
        return {
            "message": "Speaker already exists",
            "success": False
        }

    else:
        speaker.save(new_speaker_path)

    return {
        "message": "Speaker uploaded succesfully",
        "success": True
    }


# Save RVC model in RVC dir
def save_rvc(RVC_PATH, rvc):
    new_rvc_path = os.path.join(RVC_PATH, rvc.filename)

    # If path exists, return error
    if os.path.exists(new_rvc_path):
        return {
            "message": "RVC model already exists",
            "success": False
        }

    else:
        rvc.save(new_rvc_path)

    return {
        "message": "RVC model uploaded succesfully",
        "success": True
    }


# Save index in indexes dir
def save_index(INDEX_PATH, index):
    new_index_path = os.path.join(INDEX_PATH, index.filename)

    # If path exists, return error
    if os.path.exists(new_index_path):
        return {
            "message": "Index already exists",
            "success": False
        }

    else:
        index.save(new_index_path)

    return {
        "message": "Index uploaded succesfully",
        "success": True
    }


# Merge audiobook in audiobooks/BOOK/audiobook
def merge_audiobook(audiobooks_path, book):
    audiobook_dir = os.path.join(audiobooks_path, book, 'audiobook')
    audiobook_source = os.path.join(audiobooks_path, book)

    print("MERGING AUDIOBOOK: ", audiobook_dir)
    print("AUDIOBOOK SOURCE: ", audiobook_source)

    if not os.path.exists(audiobook_dir):
        os.mkdir(audiobook_dir)

    # Get params from first audio
    with wave.open(os.path.join(audiobook_source, '0.wav'), 'rb') as w:
        channels = w.getnchannels()
        sample_width = w.getsampwidth()
        frame_rate = w.getframerate()

    # Merge all audios in audiobook dir
    with wave.open(os.path.join(audiobook_dir, 'audiobook.wav'), 'wb') as output:
        # Set parameters for output
        output.setnchannels(channels)
        output.setsampwidth(sample_width)
        output.setframerate(frame_rate)

        for file in os.listdir(audiobook_source):
            if file.endswith('.wav'):
                print("MERGING: ", file)
                with wave.open(os.path.join(audiobook_source, file), 'rb') as w:
                    # Set parameters for output
                    assert (w.getnchannels(), w.getsampwidth(), w.getframerate()) == (channels, sample_width, frame_rate)
                    output.writeframes(w.readframes(w.getnframes()))

    return {
        "message": "Audiobook merged succesfully",
        "success": True
    }