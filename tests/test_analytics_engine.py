import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.analytics_engine import AnalyticsEngine

class TestAnalyticsEngine(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.analytics = AnalyticsEngine()
        # Clear any existing data
        self.analytics.grades.clear()
        self.analytics.course_grades.clear()

    def test_add_grade(self):
        """Test adding a grade"""
        result = self.analytics.add_grade("S001", "CS101", 85.5)
        self.assertTrue(result)

        # Verify grade was added
        grades = self.analytics.get_student_grades("S001")
        self.assertEqual(len(grades), 1)
        self.assertEqual(grades[0][0], "CS101")
        self.assertEqual(grades[0][1], 85.5)

    def test_student_average(self):
        """Test calculating student average"""
        self.analytics.add_grade("S001", "CS101", 80)
        self.analytics.add_grade("S001", "MATH201", 90)

        average = self.analytics.get_student_average("S001")
        self.assertEqual(average, 85.0)

    def test_top_performers(self):
        """Test getting top performers"""
        self.analytics.add_grade("S001", "CS101", 80)  # Avg: 80
        self.analytics.add_grade("S002", "CS101", 90)  # Avg: 90
        self.analytics.add_grade("S003", "CS101", 85)  # Avg: 85

        top_performers = self.analytics.get_top_performers(2)
        self.assertEqual(len(top_performers), 2)
        self.assertEqual(top_performers[0]["student_id"], "S002")  # Highest average
        self.assertEqual(top_performers[1]["student_id"], "S003")  # Second highest

    def test_course_performance(self):
        """Test course performance analysis"""
        self.analytics.add_grade("S001", "CS101", 75)
        self.analytics.add_grade("S002", "CS101", 85)
        self.analytics.add_grade("S003", "CS101", 95)

        course_avg = self.analytics.get_course_average("CS101")
        self.assertEqual(course_avg, 85.0)

        top_students = self.analytics.get_course_performance("CS101", 2)
        self.assertEqual(len(top_students), 2)
        self.assertEqual(top_students[0]["student_id"], "S003")  # Highest score
        self.assertEqual(top_students[1]["student_id"], "S002")  # Second highest

if __name__ == '__main__':
    unittest.main()
