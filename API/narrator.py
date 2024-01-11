# Narrate all lines in book
def narrate_all(lines, speaker, app):

    # Iterate lines in book
    for line in lines:

        # Check if narration is paused
        if not app.config["isNarrating"]:
            break

        # Narrate line
        narrate_line(line, speaker, line)


# Narrate single line
def narrate_line(book, speaker, line):
    print("Narrating line: ", line["line"])
