# started at 10.40am
# ended at 12.40am

import os
import sys

class Book:
    "Implementation of 'Book"
    def __init__(self, data):
        self.name = data[0].title()
        self.author = data[1].title()
        self.isbn = data[2]
        self.year = int(data[3])

    def __str__(self):
        return f"{self.name}/{self.author}/{self.isbn}/{self.year}"

def read_file(filename) -> list[Book]:
    "Read 'database'"
    books = []
    with open(filename, "r", encoding="UTF-8") as file:
        for line in file:
            book_data = line.strip().split("/")
            try:
                book = Book(book_data)
            except (IndexError, ValueError):
                print("Wrong data on line, ignoring...")
                continue
            books.append(book)
    return books

def write_file(filename, books: list):
    "Write 'database"
    with open(filename, "w", encoding="UTF-8") as file:
        for book in books:
            file.write(f"{book}\n")

def input_with_validation(text: str, validation_text: str, validation = None):
    "Input method with empty check and optional additional validation"
    while True:
        value = input(text).strip()
        if len(value) > 0 and (validation is None or validation is not None and validation(value)):
            return value
        print(validation_text)

def create_book():
    "Flow for adding a new book"
    os.system("cls")
    name = input_with_validation(
        "What is the book's name?",
        "Book name cant be empty...")
    author = input_with_validation(
        "Who is the book's author?",
        "Author cant be empty...")
    isbn = input_with_validation(
        "What is the books ISBN?",
        "ISBN must be 10 or 13 digits...",
        lambda x: x.isdigit() and len(x) in [10, 13])
    year = input_with_validation(
        "When was the book published?",
        "Year must be a digit...",
        lambda x: x.isdigit())
    return Book([name, author, isbn, year])

def main():
    # check correct amount of arguments
    if len(sys.argv) != 2:
        print("Usage: python my_library_db.py <db filename>")
        sys.exit(1)
    filename = sys.argv[1]

    # create file if it doesnt exist
    if not os.path.exists(filename):
        print("File not found, lets create one...")
        open(filename, "x", encoding="UTF-8")

    # store books into memory
    books = read_file(filename)

    # main loop of the program
    while True:
        os.system("cls")
        print("1) Add new book")
        print("2) Print current database content in asc. order by year")
        print("Q) Exit the program")
        choice = input().lower()

        if choice == "1":
            book = create_book()

            # lets force the user to validate input
            update_choice = None
            while update_choice not in ["y", "n"]:
                print(book)
                update_choice = input("Save, yes or no (y/n)?").lower()

            # add to list and sort
            if any(existing_book.isbn == book.isbn for existing_book in books):
                print(f"Book with isbn {book.isbn} already exists in the database, skipping...")
                input("Press any key to continue...")
            else:
                books.append(book)
                books.sort(key=lambda x: x.year)

        elif choice == "2":
            print(*books, sep="\n")
            input("Press any key to continue...")

        elif choice == "q":
            break

    # write books from memory into file, requires graceful shutdown
    write_file(filename, books)


if __name__ == "__main__":
    main()
