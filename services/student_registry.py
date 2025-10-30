import os
from models.student import Student
from utils.helpers import save_to_json, load_from_json
from utils.validators import validate_student_id

class StudentRegistry:
    def __init__(self, data_file="data/students.json"):
        self.students = {}  # Hash table: student_id -> Student object
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """Load student data from JSON file"""
        data = load_from_json(self.data_file)
        if data:
            for student_data in data.values():
                try:
                    student = Student.from_dict(student_data)
                    self.students[student.student_id] = student
                except Exception as e:
                    print(f"Error loading student {student_data.get('student_id')}: {e}")
            print(f"✓ Loaded {len(self.students)} students from storage")

    def _save_data(self):
        """Save student data to JSON file"""
        data = {sid: student.to_dict() for sid, student in self.students.items()}
        if save_to_json(data, self.data_file):
            return True
        return False

    def add_student(self, student_id, name, email, year=1):
        """Add a new student to the registry"""
        try:
            # Validate inputs
            if not validate_student_id(student_id):
                raise ValueError("Student ID must start with 'S' followed by numbers")

            if student_id in self.students:
                raise ValueError(f"Student {student_id} already exists")

            # Create and store student
            student = Student(student_id, name, email, year)
            self.students[student_id] = student

            # Save to persistent storage
            if self._save_data():
                return student
            else:
                # Rollback if save fails
                del self.students[student_id]
                raise Exception("Failed to save student data")

        except Exception as e:
            raise Exception(f"Failed to add student: {e}")

    def get_student(self, student_id):
        """Get student by ID - O(1) lookup"""
        if not validate_student_id(student_id):
            raise ValueError("Invalid student ID format")
        return self.students.get(student_id)

    def remove_student(self, student_id):
        """Remove student from registry"""
        try:
            if student_id not in self.students:
                raise ValueError(f"Student {student_id} not found")

            student = self.students.pop(student_id)

            if self._save_data():
                return student
            else:
                # Rollback if save fails
                self.students[student_id] = student
                raise Exception("Failed to save data after removal")

        except Exception as e:
            raise Exception(f"Failed to remove student: {e}")

    def update_student_email(self, student_id, new_email):
        """Update student email"""
        student = self.get_student(student_id)
        if student:
            old_email = student.email
            student.email = new_email
            try:
                student._validate_inputs()  # Re-validate
                if self._save_data():
                    return True
                else:
                    student.email = old_email  # Rollback
                    return False
            except ValueError as e:
                student.email = old_email  # Rollback
                raise e
        return False

    def search_students(self, name_filter=""):
        """Search students by name (case-insensitive)"""
        if not name_filter:
            return list(self.students.values())

        return [student for student in self.students.values()
                if name_filter.lower() in student.name.lower()]

    def get_all_students(self):
        """Get all students"""
        return list(self.students.values())

    def get_student_count(self):
        """Get total number of students"""
        return len(self.students)

    def student_exists(self, student_id):
        """Check if student exists"""
        return student_id in self.students

    def __str__(self):
        return f"StudentRegistry({self.get_student_count()} students)"

    def __len__(self):
        return len(self.students)
