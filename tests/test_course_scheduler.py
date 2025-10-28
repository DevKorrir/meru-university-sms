import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.course_scheduler import CourseScheduler

class TestCourseScheduler(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.scheduler = CourseScheduler("data/test_courses.json")
        # Clear any existing test data
        self.scheduler.courses.clear()

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("data/test_courses.json"):
            os.remove("data/test_courses.json")

    def test_create_course(self):
        """Test creating a course"""
        course = self.scheduler.create_course("CS101", "Data Structures", 30)
        self.assertEqual(course.course_id, "CS101")
        self.assertEqual(course.name, "Data Structures")
        self.assertEqual(course.capacity, 30)
        self.assertEqual(len(self.scheduler), 1)

    def test_enroll_student(self):
        """Test enrolling a student"""
        self.scheduler.create_course("CS101", "Data Structures", 2)

        # First enrollment should succeed
        result1 = self.scheduler.enroll_student("CS101", "S001")
        self.assertEqual(result1["status"], "enrolled")

        # Second enrollment should succeed
        result2 = self.scheduler.enroll_student("CS101", "S002")
        self.assertEqual(result2["status"], "enrolled")

        # Third enrollment should waitlist
        result3 = self.scheduler.enroll_student("CS101", "S003")
        self.assertEqual(result3["status"], "waitlisted")
        self.assertEqual(result3["position"], 1)

    def test_drop_student(self):
        """Test dropping a student"""
        self.scheduler.create_course("CS101", "Data Structures", 2)
        self.scheduler.enroll_student("CS101", "S001")
        self.scheduler.enroll_student("CS101", "S002")
        self.scheduler.enroll_student("CS101", "S003")  # Waitlisted

        # Drop enrolled student
        result = self.scheduler.drop_student("CS101", "S001")
        self.assertEqual(result["status"], "dropped")
        self.assertTrue(result["was_enrolled"])
        self.assertEqual(len(result["newly_enrolled"]), 1)  # S003 should be enrolled

    def test_course_status(self):
        """Test getting course status"""
        self.scheduler.create_course("CS101", "Data Structures", 2)
        self.scheduler.enroll_student("CS101", "S001")

        status = self.scheduler.get_course_status("CS101")
        self.assertEqual(status["course_id"], "CS101")
        self.assertEqual(status["enrolled_count"], 1)
        self.assertEqual(status["capacity"], 2)
        self.assertFalse(status["is_full"])

if __name__ == '__main__':
    unittest.main()
