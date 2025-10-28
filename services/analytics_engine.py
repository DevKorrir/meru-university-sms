import heapq
from collections import defaultdict

class AnalyticsEngine:
    def __init__(self):
        self.grades = defaultdict(list)  # student_id -> list of (course_id, score)
        self.course_grades = defaultdict(list)  # course_id -> list of (student_id, score)

    def add_grade(self, student_id, course_id, score):
        """Add a grade for analytics"""
        try:
            if not student_id or not isinstance(student_id, str):
                raise ValueError("Invalid student ID")

            if not course_id or not isinstance(course_id, str):
                raise ValueError("Invalid course ID")

            if not isinstance(score, (int, float)) or score < 0 or score > 100:
                raise ValueError("Score must be between 0 and 100")

            # Add to student's grades
            self.grades[student_id].append((course_id, score))

            # Add to course's grades
            self.course_grades[course_id].append((student_id, score))

            return True

        except Exception as e:
            raise Exception(f"Failed to add grade: {e}")

    def get_student_grades(self, student_id):
        """Get all grades for a student"""
        return self.grades.get(student_id, [])

    def get_student_average(self, student_id):
        """Calculate student's average grade"""
        grades = self.get_student_grades(student_id)
        if not grades:
            return 0.0
        return sum(score for _, score in grades) / len(grades)

    def get_course_grades(self, course_id):
        """Get all grades for a course"""
        return self.course_grades.get(course_id, [])

    def get_course_average(self, course_id):
        """Calculate course average grade"""
        grades = self.get_course_grades(course_id)
        if not grades:
            return 0.0
        return sum(score for _, score in grades) / len(grades)

    def get_top_performers(self, n=5):
        """Get top n performers using max heap"""
        # Create max heap using negative scores
        performance_heap = []

        for student_id, grades_list in self.grades.items():
            if grades_list:
                average = self.get_student_average(student_id)
                # Use negative for max heap (Python has min heap by default)
                heapq.heappush(performance_heap, (-average, student_id, grades_list))

        # Extract top n performers
        top_performers = []
        for i in range(min(n, len(performance_heap))):
            neg_avg, student_id, grades_list = heapq.heappop(performance_heap)
            top_performers.append({
                "rank": i + 1,
                "student_id": student_id,
                "average_score": -neg_avg,
                "grades": grades_list
            })

        return top_performers

    def get_course_performance(self, course_id, n=3):
        """Get top performers in a specific course"""
        grades = self.get_course_grades(course_id)
        if not grades:
            return []

        # Create max heap for course
        course_heap = []
        for student_id, score in grades:
            heapq.heappush(course_heap, (-score, student_id))

        # Extract top n
        top_students = []
        for i in range(min(n, len(course_heap))):
            neg_score, student_id = heapq.heappop(course_heap)
            top_students.append({
                "rank": i + 1,
                "student_id": student_id,
                "score": -neg_score
            })

        return top_students

    def get_student_ranking(self, student_id):
        """Get student's ranking among all students"""
        all_averages = []
        for sid in self.grades.keys():
            avg = self.get_student_average(sid)
            all_averages.append((avg, sid))

        # Sort by average (descending)
        all_averages.sort(reverse=True)

        # Find student's position
        for rank, (avg, sid) in enumerate(all_averages, 1):
            if sid == student_id:
                return {
                    "rank": rank,
                    "total_students": len(all_averages),
                    "average_score": avg
                }

        return None

    def generate_performance_report(self):
        """Generate comprehensive performance report"""
        report = {
            "total_students_with_grades": len(self.grades),
            "total_courses_with_grades": len(self.course_grades),
            "overall_average": 0.0,
            "top_performers": self.get_top_performers(5),
            "course_statistics": {}
        }

        # Calculate overall average
        total_scores = 0
        total_grades = 0
        for grades_list in self.grades.values():
            total_scores += sum(score for _, score in grades_list)
            total_grades += len(grades_list)

        if total_grades > 0:
            report["overall_average"] = total_scores / total_grades

        # Course statistics
        for course_id in self.course_grades:
            grades = self.get_course_grades(course_id)
            if grades:
                avg = self.get_course_average(course_id)
                top_students = self.get_course_performance(course_id, 3)
                report["course_statistics"][course_id] = {
                    "average_score": avg,
                    "total_grades": len(grades),
                    "top_students": top_students
                }

        return report

    def __str__(self):
        return f"AnalyticsEngine({len(self.grades)} students with grades, {len(self.course_grades)} courses with grades)"
