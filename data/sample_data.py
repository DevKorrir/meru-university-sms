"""
Sample data initialization for the School Management System
"""

def initialize_sample_data(system):
    """Initialize the system with comprehensive sample data"""

    print("Initializing sample data...")

    # Sample Students
    students = [
        ("S001", "Alice Mwangi", "alice@meru.edu", 2),
        ("S002", "Brian Kimani", "brian@meru.edu", 2),
        ("S003", "Carol Wanjiru", "carol@meru.edu", 1),
        ("S004", "David Ochieng", "david@meru.edu", 3),
        ("S005", "Eva Akinyi", "eva@meru.edu", 2),
        ("S006", "Frank Otieno", "frank@meru.edu", 4),
        ("S007", "Grace Wambui", "grace@meru.edu", 1),
        ("S008", "Henry Mutua", "henry@meru.edu", 3)
    ]

    # Sample Courses
    courses = [
        ("CS101", "Data Structures", 3),
        ("MATH201", "Calculus II", 2),
        ("PHY301", "Advanced Physics", 4),
        ("ENG101", "English Composition", 5),
        ("CHEM101", "General Chemistry", 3),
        ("BIO201", "Biology Fundamentals", 4)
    ]

    # Add students
    print("Adding sample students...")
    for student_id, name, email, year in students:
        try:
            system.student_registry.add_student(student_id, name, email, year)
            print(f"  ✓ Added student: {name}")
        except Exception as e:
            print(f"  ✗ Failed to add student {name}: {e}")

    # Create courses
    print("Creating sample courses...")
    for course_id, name, capacity in courses:
        try:
            system.course_scheduler.create_course(course_id, name, capacity)
            print(f"  ✓ Created course: {name}")
        except Exception as e:
            print(f"  ✗ Failed to create course {name}: {e}")

    # Enroll students in courses (create some waitlists)
    print("Enrolling students in courses...")
    enrollments = [
        ("CS101", "S001"), ("CS101", "S002"), ("CS101", "S003"), ("CS101", "S004"),  # S004 Waitlist
        ("MATH201", "S001"), ("MATH201", "S002"), ("MATH201", "S005"),  # S005 Waitlist
        ("PHY301", "S003"), ("PHY301", "S004"), ("PHY301", "S005"), ("PHY301", "S006"),
        ("ENG101", "S001"), ("ENG101", "S007"), ("ENG101", "S008"),
        ("CHEM101", "S002"), ("CHEM101", "S006"), ("CHEM101", "S007"),
        ("BIO201", "S003"), ("BIO201", "S005"), ("BIO201", "S008")
    ]

    for course_id, student_id in enrollments:
        try:
            result = system.course_scheduler.enroll_student(course_id, student_id)
            status = result["status"]
            if status == "waitlisted":
                print(f"  ⚠ {student_id} waitlisted for {course_id} (position: {result['position']})")
            else:
                print(f"  ✓ {student_id} enrolled in {course_id}")
        except Exception as e:
            print(f"  ✗ Failed to enroll {student_id} in {course_id}: {e}")

    # Add sample fee payments
    print("Adding sample fee payments...")
    payments = [
        ("S001", 45000, "Tuition Fee - Semester 1"),
        ("S002", 38000, "Tuition Fee - Semester 1"),
        ("S003", 50000, "Tuition Fee - Semester 1"),
        ("S004", 42000, "Tuition Fee - Semester 1"),
        ("S005", 35000, "Tuition Fee - Semester 1"),
        ("S006", 48000, "Tuition Fee - Semester 1"),
        ("S007", 39000, "Tuition Fee - Semester 1"),
        ("S008", 46000, "Tuition Fee - Semester 1"),
        ("S001", 5000, "Library Fee"),
        ("S002", 5000, "Library Fee"),
        ("S003", 5000, "Library Fee")
    ]

    for student_id, amount, description in payments:
        try:
            transaction = system.fee_tracker.add_payment(student_id, amount, description)
            print(f"  ✓ Payment of ${amount:,} for {student_id}")
        except Exception as e:
            print(f"  ✗ Failed to add payment for {student_id}: {e}")

    # Add library books
    print("Adding library books...")
    books = [
        ("ISBN001", "Introduction to Algorithms", "Thomas Cormen", 3),
        ("ISBN002", "Calculus Made Easy", "Silvanus Thompson", 2),
        ("ISBN003", "Python Programming", "John Smith", 4),
        ("ISBN004", "Physics for Scientists", "Paul Hewitt", 1),
        ("ISBN005", "Chemistry: The Central Science", "Theodore Brown", 2),
        ("ISBN006", "Biology: Concepts and Connections", "Neil Campbell", 3)
    ]

    for isbn, title, author, copies in books:
        try:
            system.library_system.add_book(isbn, title, author, copies)
            print(f"  ✓ Added book: {title}")
        except Exception as e:
            print(f"  ✗ Failed to add book {title}: {e}")

    # Simulate some book borrow/return activity
    print("Simulating library activity...")
    library_actions = [
        ("ISBN001", "S001", "borrow"),
        ("ISBN001", "S002", "borrow"),
        ("ISBN002", "S003", "borrow"),
        ("ISBN003", "S001", "borrow"),
        ("ISBN001", "S001", "return"),
        ("ISBN004", "S004", "borrow")
    ]

    for isbn, student_id, action in library_actions:
        try:
            if action == "borrow":
                result = system.library_system.borrow_book(isbn, student_id)
                if result["success"]:
                    print(f"  ✓ {student_id} borrowed {isbn}")
                else:
                    print(f"  ✗ {student_id} failed to borrow {isbn}: {result['message']}")
            elif action == "return":
                result = system.library_system.return_book(isbn, student_id)
                if result["success"]:
                    print(f"  ✓ {student_id} returned {isbn}")
                else:
                    print(f"  ✗ {student_id} failed to return {isbn}: {result['message']}")
        except Exception as e:
            print(f"  ✗ Library action failed: {e}")

    # Add sample grades for analytics
    print("Adding sample grades...")
    grades = [
        # CS101 grades
        ("S001", "CS101", 85), ("S002", "CS101", 78), ("S003", "CS101", 92),
        ("S004", "CS101", 88),
        # MATH201 grades
        ("S001", "MATH201", 90), ("S002", "MATH201", 82), ("S005", "MATH201", 95),
        # PHY301 grades
        ("S003", "PHY301", 87), ("S004", "PHY301", 91), ("S005", "PHY301", 84), ("S006", "PHY301", 89),
        # ENG101 grades
        ("S001", "ENG101", 88), ("S007", "ENG101", 76), ("S008", "ENG101", 92),
        # CHEM101 grades
        ("S002", "CHEM101", 81), ("S006", "CHEM101", 79), ("S007", "CHEM101", 85),
        # BIO201 grades
        ("S003", "BIO201", 94), ("S005", "BIO201", 87), ("S008", "BIO201", 90)
    ]

    for student_id, course_id, score in grades:
        try:
            system.analytics_engine.add_grade(student_id, course_id, score)
            print(f"  ✓ Grade added: {student_id} - {course_id} = {score}")
        except Exception as e:
            print(f"  ✗ Failed to add grade for {student_id}: {e}")

    print("\n" + "="*50)
    print("Sample data initialization complete!")
    print("="*50)
    print(f"Students: {len(system.student_registry)}")
    print(f"Courses: {len(system.course_scheduler)}")
    print(f"Transactions: {len(system.fee_tracker)}")
    print(f"Books: {len(system.library_system)}")
    print(f"Grades recorded: {sum(len(grades) for grades in system.analytics_engine.grades.values())}")
    print("="*50)
