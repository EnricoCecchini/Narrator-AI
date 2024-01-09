import os

# Save book and parse into individual files for each sentence
def save_book(BOOKS_PATH, book):
    # Make path for uploaded book
    new_book_path = os.path.join(BOOKS_PATH, book.filename.replace(".txt", ""))
    processed_path = os.path.join(new_book_path, "Processed")

    # If path exists, return error
    if os.path.exists(new_book_path):
        return {"message": "Book already exists", "success": False}

    else:
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