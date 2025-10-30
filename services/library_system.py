import os
from models.book import Book
from utils.helpers import save_to_json, load_from_json
from utils.validators import validate_isbn

class LibrarySystem:
    def __init__(self, data_file="data/books.json"):
        self.books = {}  # Hash table: isbn -> Book object
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """Load book data from JSON file"""
        data = load_from_json(self.data_file)
        if data:
            for book_data in data.values():
                try:
                    book = Book.from_dict(book_data)
                    self.books[book.isbn] = book
                except Exception as e:
                    print(f"Error loading book {book_data.get('isbn')}: {e}")
            print(f"✓ Loaded {len(self.books)} books from storage")

    def _save_data(self):
        """Save book data to JSON file"""
        data = {isbn: book.to_dict() for isbn, book in self.books.items()}
        if save_to_json(data, self.data_file):
            return True
        return False

    def add_book(self, isbn, title, author, total_copies):
        """Add a new book to the library"""
        try:
            if not validate_isbn(isbn):
                raise ValueError("Invalid ISBN format")

            if isbn in self.books:
                raise ValueError(f"Book with ISBN {isbn} already exists")

            book = Book(isbn, title, author, total_copies)
            self.books[isbn] = book

            if self._save_data():
                return book
            else:
                del self.books[isbn]
                raise Exception("Failed to save book data")

        except Exception as e:
            raise Exception(f"Failed to add book: {e}")

    def borrow_book(self, isbn, student_id):
        """Borrow a book copy"""
        try:
            if isbn not in self.books:
                raise ValueError("Book not found")

            book = self.books[isbn]

            if book.available_copies <= 0:
                return {"success": False, "message": "No copies available"}

            success = book.borrow_book(student_id)
            if success:
                if self._save_data():
                    return {
                        "success": True,
                        "message": f"Successfully borrowed '{book.title}'",
                        "available_copies": book.available_copies
                    }
                else:
                    # Rollback borrow operation
                    book.available_copies += 1
                    if book.borrow_history and book.borrow_history[-1]['student_id'] == student_id:
                        book.borrow_history.pop()
                    return {"success": False, "message": "Failed to save borrow data"}
            else:
                return {"success": False, "message": "Borrow operation failed"}

        except Exception as e:
            raise Exception(f"Failed to borrow book: {e}")

    def return_book(self, isbn, student_id):
        """Return a book copy"""
        try:
            if isbn not in self.books:
                raise ValueError("Book not found")

            book = self.books[isbn]

            if book.available_copies >= book.total_copies:
                return {"success": False, "message": "All copies are already available"}

            success = book.return_book(student_id)
            if success:
                if self._save_data():
                    return {
                        "success": True,
                        "message": f"Successfully returned '{book.title}'",
                        "available_copies": book.available_copies
                    }
                else:
                    # Rollback return operation
                    book.available_copies -= 1
                    if book.borrow_history and book.borrow_history[-1]['student_id'] == student_id:
                        book.borrow_history.pop()
                    return {"success": False, "message": "Failed to save return data"}
            else:
                return {"success": False, "message": "Return operation failed"}

        except Exception as e:
            raise Exception(f"Failed to return book: {e}")

    def get_book(self, isbn):
        """Get book by ISBN"""
        return self.books.get(isbn)

    def search_books(self, title_filter="", author_filter=""):
        """Search books by title and/or author"""
        results = []
        for book in self.books.values():
            title_match = not title_filter or title_filter.lower() in book.title.lower()
            author_match = not author_filter or author_filter.lower() in book.author.lower()

            if title_match and author_match:
                results.append(book)

        return results

    def get_available_books(self):
        """Get all books with available copies"""
        return [book for book in self.books.values() if book.available_copies > 0]

    def get_book_status(self, isbn):
        """Get detailed book status"""
        book = self.get_book(isbn)
        if not book:
            return None

        return {
            "isbn": book.isbn,
            "title": book.title,
            "author": book.author,
            "total_copies": book.total_copies,
            "available_copies": book.available_copies,
            "borrowed_copies": book.total_copies - book.available_copies,
            "recent_activity": book.get_recent_activity(5)
        }

    def __str__(self):
        available = len(self.get_available_books())
        return f"LibrarySystem({len(self.books)} books, {available} available)"

    def __len__(self):
        return len(self.books)
