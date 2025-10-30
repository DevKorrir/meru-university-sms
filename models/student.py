from utils.validators import validate_email, validate_year

class Student:
    def __init__(self, student_id, name, email, year=1):
        self.student_id = student_id
        self.name = name
        self.email = email
        self.year = year
        self.courses = []
        self.fees_paid = 0

        # Validate inputs
        self._validate_inputs()

    def _validate_inputs(self):
        """Validate student data"""
        if not self.student_id or not isinstance(self.student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if not self.name or not isinstance(self.name, str):
            raise ValueError("Name must be a non-empty string")

        if not validate_email(self.email):
            raise ValueError("Invalid email format")

        if not validate_year(self.year):
            raise ValueError("Year must be between 1 and 5")

    def add_course(self, course_id):
        """Add course to student's course list"""
        if not course_id or not isinstance(course_id, str):
            raise ValueError("Course ID must be a non-empty string")

        if course_id not in self.courses:
            self.courses.append(course_id)
            return True
        return False

    def add_payment(self, amount):
        """Add payment to student's total fees paid"""
        if not isinstance(amount, (int, float)) or amount < 0:
            raise ValueError("Amount must be a positive number")

        self.fees_paid += amount
        return self.fees_paid

    def to_dict(self):
        """Convert student to dictionary for JSON serialization"""
        return {
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'year': self.year,
            'courses': self.courses,
            'fees_paid': self.fees_paid
        }

    @classmethod
    def from_dict(cls, data):
        """Create student from dictionary"""
        student = cls(
            data['student_id'],
            data['name'],
            data['email'],
            data['year']
        )
        student.courses = data.get('courses', [])
        student.fees_paid = data.get('fees_paid', 0)
        return student

    def __str__(self):
        return f"Student(ID: {self.student_id}, Name: {self.name}, Email: {self.email}, Year: {self.year})"

    def __repr__(self):
        return f"Student({self.student_id}, {self.name}, {self.email}, {self.year})"
