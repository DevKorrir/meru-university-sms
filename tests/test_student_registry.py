import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.student_registry import StudentRegistry
from models.student import Student

class TestStudentRegistry(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.registry = StudentRegistry("data/test_students.json")
        # Clear any existing test data
        self.registry.students.clear()

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("data/test_students.json"):
            os.remove("data/test_students.json")

    def test_add_student(self):
        """Test adding a student"""
        student = self.registry.add_student("S001", "John Doe", "john@meru.edu", 2)
        self.assertIsInstance(student, Student)
        self.assertEqual(student.student_id, "S001")
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(self.registry.get_student_count(), 1)

    def test_add_duplicate_student(self):
        """Test adding duplicate student"""
        self.registry.add_student("S001", "John Doe", "john@meru.edu", 2)
        with self.assertRaises(Exception):
            self.registry.add_student("S001", "Jane Doe", "jane@meru.edu", 1)

    def test_get_student(self):
        """Test retrieving student"""
        self.registry.add_student("S001", "John Doe", "john@meru.edu", 2)
        student = self.registry.get_student("S001")
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(student.email, "john@meru.edu")

    def test_remove_student(self):
        """Test removing student"""
        self.registry.add_student("S001", "John Doe", "john@meru.edu", 2)
        student = self.registry.remove_student("S001")
        self.assertEqual(student.name, "John Doe")
        self.assertEqual(self.registry.get_student_count(), 0)

    def test_search_students(self):
        """Test student search functionality"""
        self.registry.add_student("S001", "John Doe", "john@meru.edu", 2)
        self.registry.add_student("S002", "Jane Smith", "jane@meru.edu", 1)

        results = self.registry.search_students("John")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")

        results = self.registry.search_students("Doe")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "John Doe")

if __name__ == '__main__':
    unittest.main()
