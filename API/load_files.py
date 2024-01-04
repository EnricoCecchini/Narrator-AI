import os

# Load list of speakers in dir
def load_speakers(SPEAKERS_PATH):
    speakers = []
    for file in os.listdir(SPEAKERS_PATH):
        if file.endswith(".wav"):
            speakers.append(file)
    
    print(SPEAKERS_PATH, speakers)
    
    return speakers

# Load list of books in dir
def load_books(BOOKS_PATH):
    books = []
    print(BOOKS_PATH, books)
    for file in os.listdir(BOOKS_PATH):
        books.append(file)
    
    #print(BOOKS_PATH, books)
    
    return books

# Load list of audiobooks in dir
def load_audiobooks(AUDIOBOOKS_PATH):
    audiobooks = []
    for file in os.listdir(AUDIOBOOKS_PATH):
        if file.endswith(".wav"):
            audiobooks.append(file)
    
    print(AUDIOBOOKS_PATH, audiobooks)

    return audiobooks

# Load list of RVC models in dir
def load_rvc_models(RVC_PATH):
    rvc_models = []
    for file in os.listdir(RVC_PATH):
        rvc_models.append(file)
    
    print(RVC_PATH, rvc_models)
    
    return rvc_models


# Load lines in selected book
def load_selected_book(BOOKS_PATH, book):
    pass