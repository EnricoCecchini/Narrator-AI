import os

def save_book(BOOKS_PATH, book):
    print('SAVING BOOK: ', book)
    # Make path for uploaded book
    new_book_path = os.path.join(BOOKS_PATH, book.filename.replace(".txt", ""))
    processed_path = os.path.join(new_book_path, "Processed")
    print(new_book_path)
    print('SAVING BOOK PROCESSED: ', processed_path)

    # If path exists, return error
    if os.path.exists(new_book_path):
        return {"message": "Book already exists", "success": False}
    
    else:
        os.makedirs(new_book_path)
        os.makedirs(processed_path)
    
    # Save OG book
    book.save(os.path.join(new_book_path, book.filename))

    book_path = os.path.join(new_book_path, book.filename)
    print('READ: ', book_path)

    # Read book and split into lines in separate files in Processed dir
    with open(book_path, 'r') as file:
        lines = file.readlines()
        # Skip empty lines

        print(lines)
        for i, line in enumerate(lines):
            print(os.path.join(processed_path, f"{i}.txt"))
            with open(os.path.join(processed_path, f"{i}.txt"), 'w') as f:
                f.write(line)
    
    return {"message": "Book uploaded and processed succesfully", "success": True}