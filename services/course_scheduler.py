import os
from models.course import Course
from utils.helpers import save_to_json, load_from_json
from utils.validators import validate_course_id

class CourseScheduler:
    def __init__(self, data_file="data/courses.json"):
        self.courses = {}  # course_id -> Course object
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """Load course data from JSON file"""
        data = load_from_json(self.data_file)
        if data:
            for course_data in data.values():
                try:
                    course = Course.from_dict(course_data)
                    self.courses[course.course_id] = course
                except Exception as e:
                    print(f"Error loading course {course_data.get('course_id')}: {e}")
            print(f"✓ Loaded {len(self.courses)} courses from storage")

    def _save_data(self):
        """Save course data to JSON file"""
        data = {cid: course.to_dict() for cid, course in self.courses.items()}
        if save_to_json(data, self.data_file):
            return True
        return False

    def create_course(self, course_id, name, capacity):
        """Create a new course"""
        try:
            if not validate_course_id(course_id):
                raise ValueError("Invalid course ID format")

            if course_id in self.courses:
                raise ValueError(f"Course {course_id} already exists")

            course = Course(course_id, name, capacity)
            self.courses[course_id] = course

            if self._save_data():
                return course
            else:
                del self.courses[course_id]
                raise Exception("Failed to save course data")

        except Exception as e:
            raise Exception(f"Failed to create course: {e}")

    def enroll_student(self, course_id, student_id):
        """Enroll student in course with waitlist handling"""
        try:
            if course_id not in self.courses:
                raise ValueError("Course not found")

            course = self.courses[course_id]

            # Check if already enrolled
            if student_id in course.enrolled_students:
                return {"status": "already_enrolled", "position": 0}

            # Check capacity
            if not course.is_full():
                course.enroll_student(student_id)
                if self._save_data():
                    return {"status": "enrolled", "position": 0}
                else:
                    # Rollback enrollment
                    course.enrolled_students.remove(student_id)
                    raise Exception("Failed to save enrollment data")
            else:
                # Add to waitlist
                position = course.add_to_waitlist(student_id)
                if self._save_data():
                    return {"status": "waitlisted", "position": position}
                else:
                    # Rollback waitlist addition
                    if student_id in course.waitlist:
                        course.waitlist.remove(student_id)
                    raise Exception("Failed to save waitlist data")

        except Exception as e:
            raise Exception(f"Failed to enroll student: {e}")

    def drop_student(self, course_id, student_id):
        """Drop student from course and process waitlist"""
        try:
            if course_id not in self.courses:
                raise ValueError("Course not found")

            course = self.courses[course_id]
            enrolled = student_id in course.enrolled_students
            waitlisted = student_id in course.waitlist

            if not enrolled and not waitlisted:
                return {"status": "not_found", "message": "Student not enrolled or waitlisted"}

            result = {"status": "dropped"}

            if enrolled:
                course.enrolled_students.remove(student_id)
                result["was_enrolled"] = True

                # Process waitlist if there was a vacancy
                newly_enrolled = self._process_waitlist(course_id)
                result["newly_enrolled"] = newly_enrolled

            elif waitlisted:
                course.waitlist.remove(student_id)
                result["was_waitlisted"] = True

            if self._save_data():
                return result
            else:
                raise Exception("Failed to save data after drop")

        except Exception as e:
            raise Exception(f"Failed to drop student: {e}")

    def _process_waitlist(self, course_id):
        """Process waitlist for a course (internal method)"""
        course = self.courses[course_id]
        newly_enrolled = []

        while course.waitlist and not course.is_full():
            student_id = course.waitlist.popleft()
            course.enroll_student(student_id)
            newly_enrolled.append(student_id)

        return newly_enrolled

    def get_course_status(self, course_id):
        """Get detailed course status"""
        if course_id not in self.courses:
            return None

        course = self.courses[course_id]
        return {
            "course_id": course.course_id,
            "name": course.name,
            "capacity": course.capacity,
            "enrolled_count": len(course.enrolled_students),
            "waitlist_count": len(course.waitlist),
            "is_full": course.is_full(),
            "enrolled_students": list(course.enrolled_students),
            "waitlist": list(course.waitlist)
        }

    def get_waitlist_position(self, course_id, student_id):
        """Get student's position in course waitlist"""
        if course_id not in self.courses:
            return -1
        return self.courses[course_id].get_waitlist_position(student_id)

    def get_all_courses(self):
        """Get all courses"""
        return list(self.courses.values())

    def course_exists(self, course_id):
        """Check if course exists"""
        return course_id in self.courses

    def __str__(self):
        return f"CourseScheduler({len(self.courses)} courses)"

    def __len__(self):
        return len(self.courses)
