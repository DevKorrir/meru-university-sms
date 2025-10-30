from collections import deque
from utils.validators import validate_capacity

class Course:
    def __init__(self, course_id, name, capacity):
        self.course_id = course_id
        self.name = name
        self.capacity = capacity
        self.enrolled_students = []
        self.waitlist = deque()

        self._validate_inputs()

    def _validate_inputs(self):
        """Validate course data"""
        if not self.course_id or not isinstance(self.course_id, str):
            raise ValueError("Course ID must be a non-empty string")

        if not self.name or not isinstance(self.name, str):
            raise ValueError("Course name must be a non-empty string")

        if not validate_capacity(self.capacity):
            raise ValueError("Capacity must be a positive integer")

    def is_full(self):
        """Check if course is at capacity"""
        return len(self.enrolled_students) >= self.capacity

    def add_to_waitlist(self, student_id):
        """Add student to waitlist"""
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if student_id not in self.waitlist:
            self.waitlist.append(student_id)
            return len(self.waitlist)
        return -1

    def enroll_student(self, student_id):
        """Enroll student directly"""
        if not student_id or not isinstance(student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if student_id not in self.enrolled_students:
            self.enrolled_students.append(student_id)
            return True
        return False

    def get_waitlist_position(self, student_id):
        """Get student's position in waitlist"""
        try:
            return list(self.waitlist).index(student_id) + 1
        except ValueError:
            return -1

    def to_dict(self):
        """Convert course to dictionary for JSON serialization"""
        return {
            'course_id': self.course_id,
            'name': self.name,
            'capacity': self.capacity,
            'enrolled_students': list(self.enrolled_students),
            'waitlist': list(self.waitlist)
        }

    @classmethod
    def from_dict(cls, data):
        """Create course from dictionary"""
        course = cls(
            data['course_id'],
            data['name'],
            data['capacity']
        )
        course.enrolled_students = data.get('enrolled_students', [])
        course.waitlist = deque(data.get('waitlist', []))
        return course

    def __str__(self):
        return f"Course(ID: {self.course_id}, Name: {self.name}, Capacity: {self.capacity})"
