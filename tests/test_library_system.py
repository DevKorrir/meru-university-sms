import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.library_system import LibrarySystem

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.library = LibrarySystem("data/test_books.json")
        # Clear any existing test data
        self.library.books.clear()

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("data/test_books.json"):
            os.remove("data/test_books.json")

    def test_add_book(self):
        """Test adding a book"""
        book = self.library.add_book("ISBN001", "Test Book", "Test Author", 3)
        self.assertEqual(book.isbn, "ISBN001")
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.total_copies, 3)
        self.assertEqual(book.available_copies, 3)
        self.assertEqual(len(self.library), 1)

    def test_borrow_book(self):
        """Test borrowing a book"""
        self.library.add_book("ISBN001", "Test Book", "Test Author", 2)

        # First borrow should succeed
        result1 = self.library.borrow_book("ISBN001", "S001")
        self.assertTrue(result1["success"])
        self.assertEqual(result1["available_copies"], 1)

        # Second borrow should succeed
        result2 = self.library.borrow_book("ISBN001", "S002")
        self.assertTrue(result2["success"])
        self.assertEqual(result2["available_copies"], 0)

        # Third borrow should fail
        result3 = self.library.borrow_book("ISBN001", "S003")
        self.assertFalse(result3["success"])
        self.assertEqual(result3["message"], "No copies available")

    def test_return_book(self):
        """Test returning a book"""
        self.library.add_book("ISBN001", "Test Book", "Test Author", 2)
        self.library.borrow_book("ISBN001", "S001")

        # Return should succeed
        result = self.library.return_book("ISBN001", "S001")
        self.assertTrue(result["success"])
        self.assertEqual(result["available_copies"], 2)

        # Return when all copies are available should fail
        result2 = self.library.return_book("ISBN001", "S001")
        self.assertFalse(result2["success"])

    def test_search_books(self):
        """Test book search functionality"""
        self.library.add_book("ISBN001", "Python Programming", "John Smith", 2)
        self.library.add_book("ISBN002", "Java Basics", "Jane Doe", 1)

        # Search by title
        python_books = self.library.search_books("Python", "")
        self.assertEqual(len(python_books), 1)
        self.assertEqual(python_books[0].title, "Python Programming")

        # Search by author
        smith_books = self.library.search_books("", "Smith")
        self.assertEqual(len(smith_books), 1)
        self.assertEqual(smith_books[0].author, "John Smith")

if __name__ == '__main__':
    unittest.main()
