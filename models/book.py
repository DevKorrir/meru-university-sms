from utils.validators import validate_isbn

class Book:
    def __init__(self, isbn, title, author, total_copies):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = total_copies
        self.available_copies = total_copies
        self.borrow_history = []

        self._validate_inputs()

    def _validate_inputs(self):
        """Validate book data"""
        if not validate_isbn(self.isbn):
            raise ValueError("Invalid ISBN format")

        if not self.title or not isinstance(self.title, str):
            raise ValueError("Title must be a non-empty string")

        if not self.author or not isinstance(self.author, str):
            raise ValueError("Author must be a non-empty string")

        if not isinstance(self.total_copies, int) or self.total_copies <= 0:
            raise ValueError("Total copies must be a positive integer")

    def borrow_book(self, student_id):
        """Borrow a book copy"""
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if self.available_copies > 0:
            self.available_copies -= 1
            self.borrow_history.append({
                'student_id': student_id,
                'action': 'borrowed',
                'timestamp': self._get_timestamp()
            })
            return True
        return False

    def return_book(self, student_id):
        """Return a book copy"""
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if self.available_copies < self.total_copies:
            self.available_copies += 1
            self.borrow_history.append({
                'student_id': student_id,
                'action': 'returned',
                'timestamp': self._get_timestamp()
            })
            return True
        return False

    def _get_timestamp(self):
        """Get current timestamp (simplified)"""
        from datetime import datetime
        return datetime.now().isoformat()

    def get_recent_activity(self, limit=5):
        """Get recent borrow/return activity"""
        return self.borrow_history[-limit:] if self.borrow_history else []

    def to_dict(self):
        """Convert book to dictionary for JSON serialization"""
        return {
            'isbn': self.isbn,
            'title': self.title,
            'author': self.author,
            'total_copies': self.total_copies,
            'available_copies': self.available_copies,
            'borrow_history': self.borrow_history
        }

    @classmethod
    def from_dict(cls, data):
        """Create book from dictionary"""
        book = cls(
            data['isbn'],
            data['title'],
            data['author'],
            data['total_copies']
        )
        book.available_copies = data.get('available_copies', data['total_copies'])
        book.borrow_history = data.get('borrow_history', [])
        return book

    def __str__(self):
        return f"Book(ISBN: {self.isbn}, Title: {self.title}, Available: {self.available_copies}/{self.total_copies})"
