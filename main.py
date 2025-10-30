#!/usr/bin/env python3
"""
Main application for Meru University School Management System
"""

import os
import sys
from services.student_registry import StudentRegistry
from services.course_scheduler import CourseScheduler
from services.fee_tracker import FeeTracker
from services.library_system import LibrarySystem
from services.analytics_engine import AnalyticsEngine
from data.sample_data import initialize_sample_data

class SchoolManagementSystem:
    def __init__(self):
        """Initialize the school management system with all modules"""
        print("Initializing Meru University School Management System...")
        
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Initialize all modules
        self.student_registry = StudentRegistry()
        self.course_scheduler = CourseScheduler()
        self.fee_tracker = FeeTracker()
        self.library_system = LibrarySystem()
        self.analytics_engine = AnalyticsEngine()
        
        print("✓ All modules initialized successfully")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*60)
        print("🏫 MERU UNIVERSITY SCHOOL MANAGEMENT SYSTEM")
        print("="*60)
        print("1. Student Management")
        print("2. Course Management")
        print("3. Fee Management")
        print("4. Library Management")
        print("5. Analytics & Reports")
        print("6. System Demo")
        print("7. Exit")
        print("="*60)
    
    def student_management_menu(self):
        """Student management submenu"""
        while True:
            print("\n--- STUDENT MANAGEMENT ---")
            print("1. Add Student")
            print("2. Find Student")
            print("3. Remove Student")
            print("4. List All Students")
            print("5. Search Students")
            print("6. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_student()
            elif choice == '2':
                self.find_student()
            elif choice == '3':
                self.remove_student()
            elif choice == '4':
                self.list_all_students()
            elif choice == '5':
                self.search_students()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_student(self):
        """Add a new student"""
        print("\n--- ADD NEW STUDENT ---")
        try:
            student_id = input("Student ID (format SXXX): ").strip()
            name = input("Full Name: ").strip()
            email = input("Email: ").strip()
            year = int(input("Year (1-5): ").strip())
            
            student = self.student_registry.add_student(student_id, name, email, year)
            print(f"✓ Student added successfully: {student}")
            
        except ValueError as e:
            print(f"✗ Invalid input: {e}")
        except Exception as e:
            print(f"✗ Error adding student: {e}")
    
    def find_student(self):
        """Find student by ID"""
        print("\n--- FIND STUDENT ---")
        student_id = input("Enter Student ID: ").strip()
        
        student = self.student_registry.get_student(student_id)
        if student:
            print(f"✓ Student found: {student}")
            print(f"  Email: {student.email}")
            print(f"  Year: {student.year}")
            print(f"  Courses: {', '.join(student.courses) if student.courses else 'None'}")
            print(f"  Fees Paid: Ksh.{student.fees_paid:,.2f}")
        else:
            print("✗ Student not found")
    
    def remove_student(self):
        """Remove a student"""
        print("\n--- REMOVE STUDENT ---")
        student_id = input("Enter Student ID to remove: ").strip()
        
        try:
            student = self.student_registry.remove_student(student_id)
            print(f"✓ Student removed: {student.name}")
        except Exception as e:
            print(f"✗ Error removing student: {e}")
    
    def list_all_students(self):
        """List all students"""
        students = self.student_registry.get_all_students()
        if not students:
            print("No students registered.")
            return
        
        print(f"\n--- ALL STUDENTS ({len(students)} total) ---")
        for student in students:
            print(f"{student.student_id}: {student.name} | {student.email} | Year {student.year}")
    
    def search_students(self):
        """Search students by name"""
        print("\n--- SEARCH STUDENTS ---")
        name_filter = input("Enter name to search (leave empty for all): ").strip()
        
        students = self.student_registry.search_students(name_filter)
        if not students:
            print("No students found matching your criteria.")
            return
        
        print(f"\n--- SEARCH RESULTS ({len(students)} found) ---")
        for student in students:
            print(f"{student.student_id}: {student.name} | {student.email}")
    
    def course_management_menu(self):
        """Course management submenu"""
        while True:
            print("\n--- COURSE MANAGEMENT ---")
            print("1. Create Course")
            print("2. Enroll Student")
            print("3. Drop Student")
            print("4. Course Status")
            print("5. List All Courses")
            print("6. Process Waitlist")
            print("7. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.create_course()
            elif choice == '2':
                self.enroll_student()
            elif choice == '3':
                self.drop_student()
            elif choice == '4':
                self.course_status()
            elif choice == '5':
                self.list_all_courses()
            elif choice == '6':
                self.process_waitlist()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def create_course(self):
        """Create a new course"""
        print("\n--- CREATE COURSE ---")
        try:
            course_id = input("Course ID: ").strip()
            name = input("Course Name: ").strip()
            capacity = int(input("Capacity: ").strip())
            
            course = self.course_scheduler.create_course(course_id, name, capacity)
            print(f"✓ Course created: {course}")
            
        except ValueError as e:
            print(f"✗ Invalid input: {e}")
        except Exception as e:
            print(f"✗ Error creating course: {e}")
    
    def enroll_student(self):
        """Enroll student in course"""
        print("\n--- ENROLL STUDENT ---")
        try:
            course_id = input("Course ID: ").strip()
            student_id = input("Student ID: ").strip()
            
            result = self.course_scheduler.enroll_student(course_id, student_id)
            
            if result["status"] == "enrolled":
                print("✓ Student enrolled successfully")
            elif result["status"] == "waitlisted":
                print(f"⚠ Student added to waitlist (position: {result['position']})")
            elif result["status"] == "already_enrolled":
                print("ℹ Student already enrolled in this course")
                
        except Exception as e:
            print(f"✗ Error enrolling student: {e}")
    
    def drop_student(self):
        """Drop student from course"""
        print("\n--- DROP STUDENT ---")
        try:
            course_id = input("Course ID: ").strip()
            student_id = input("Student ID: ").strip()
            
            result = self.course_scheduler.drop_student(course_id, student_id)
            
            if result["status"] == "dropped":
                message = "Student dropped from course"
                if result.get("was_enrolled"):
                    message += " (was enrolled)"
                elif result.get("was_waitlisted"):
                    message += " (was waitlisted)"
                
                if result.get("newly_enrolled"):
                    message += f"\n✓ {len(result['newly_enrolled'])} students enrolled from waitlist"
                
                print(f"✓ {message}")
            else:
                print(f"ℹ {result['message']}")
                
        except Exception as e:
            print(f"✗ Error dropping student: {e}")
    
    def course_status(self):
        """Display course status"""
        print("\n--- COURSE STATUS ---")
        course_id = input("Enter Course ID: ").strip()
        
        status = self.course_scheduler.get_course_status(course_id)
        if status:
            print(f"\nCourse: {status['name']} ({status['course_id']})")
            print(f"Capacity: {status['enrolled_count']}/{status['capacity']}")
            print(f"Waitlist: {status['waitlist_count']} students")
            print(f"Status: {'FULL' if status['is_full'] else 'AVAILABLE'}")
            
            if status['enrolled_students']:
                print(f"\nEnrolled Students: {', '.join(status['enrolled_students'])}")
            if status['waitlist']:
                print(f"Waitlist: {', '.join(status['waitlist'])}")
        else:
            print("✗ Course not found")
    
    def list_all_courses(self):
        """List all courses"""
        courses = self.course_scheduler.get_all_courses()
        if not courses:
            print("No courses available.")
            return
        
        print(f"\n--- ALL COURSES ({len(courses)} total) ---")
        for course in courses:
            status = "FULL" if course.is_full() else "AVAILABLE"
            print(f"{course.course_id}: {course.name} | {len(course.enrolled_students)}/{course.capacity} | {status}")
    
    def process_waitlist(self):
        """Process course waitlist"""
        print("\n--- PROCESS WAITLIST ---")
        course_id = input("Enter Course ID: ").strip()
        
        try:
            # This is typically automatic, but we can force process
            course = self.course_scheduler.courses.get(course_id)
            if not course:
                print("✗ Course not found")
                return
            
            newly_enrolled = self.course_scheduler._process_waitlist(course_id)
            if newly_enrolled:
                print(f"✓ {len(newly_enrolled)} students enrolled from waitlist:")
                for student_id in newly_enrolled:
                    print(f"  - {student_id}")
                self.course_scheduler._save_data()
            else:
                print("ℹ No students to enroll from waitlist")
                
        except Exception as e:
            print(f"✗ Error processing waitlist: {e}")
    
    def fee_management_menu(self):
        """Fee management submenu"""
        while True:
            print("\n--- FEE MANAGEMENT ---")
            print("1. Add Payment")
            print("2. View Transaction")
            print("3. Student Payment History")
            print("4. Generate Clearance Report")
            print("5. View All Transactions")
            print("6. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.add_payment()
            elif choice == '2':
                self.view_transaction()
            elif choice == '3':
                self.student_payment_history()
            elif choice == '4':
                self.generate_clearance_report()
            elif choice == '5':
                self.view_all_transactions()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_payment(self):
        """Add a payment transaction"""
        print("\n--- ADD PAYMENT ---")
        try:
            student_id = input("Student ID: ").strip()
            amount = float(input("Amount: ").strip())
            description = input("Description: ").strip() or "Tuition Fee"
            
            transaction = self.fee_tracker.add_payment(student_id, amount, description)
            print(f"✓ Payment recorded: {transaction}")
            
            # Update student's total fees
            student = self.student_registry.get_student(student_id)
            if student:
                student.add_payment(amount)
                self.student_registry._save_data()
                
        except ValueError as e:
            print(f"✗ Invalid input: {e}")
        except Exception as e:
            print(f"✗ Error adding payment: {e}")
    
    def view_transaction(self):
        """View transaction by ID"""
        print("\n--- VIEW TRANSACTION ---")
        transaction_id = input("Transaction ID: ").strip()
        
        transaction = self.fee_tracker.get_transaction(transaction_id)
        if transaction:
            print(f"✓ Transaction found:")
            print(f"  ID: {transaction.transaction_id}")
            print(f"  Student: {transaction.student_id}")
            print(f"  Amount: ksh.{transaction.amount:,.2f}")
            print(f"  Date: {transaction.date}")
            print(f"  Description: {transaction.description}")
        else:
            print("✗ Transaction not found")
    
    def student_payment_history(self):
        """View student's payment history"""
        print("\n--- STUDENT PAYMENT HISTORY ---")
        student_id = input("Student ID: ").strip()
        
        transactions = self.fee_tracker.get_student_transactions(student_id)
        if not transactions:
            print("No transactions found for this student.")
            return
        
        total_paid = sum(tx.amount for tx in transactions)
        print(f"\nPayment History for {student_id}:")
        print(f"Total Paid: Ksh.{total_paid:,.2f}")
        print("\nTransactions:")
        for tx in transactions:
            print(f"  {tx.date}: Ksh.{tx.amount:,.2f} - {tx.description}")
    
    def generate_clearance_report(self):
        """Generate fee clearance report"""
        print("\n--- FEE CLEARANCE REPORT ---")
        try:
            required_amount = float(input("Enter required fee amount: ").strip())
            
            report = self.fee_tracker.generate_clearance_report(required_amount)
            
            print(f"\n=== FEE CLEARANCE REPORT ===")
            print(f"Required Amount: Ksh.{required_amount:,.2f}")
            print(f"Clearance Rate: {report['clearance_rate']:.1%}")
            
            print(f"\nCLEARED STUDENTS ({len(report['cleared_students'])}):")
            for student in report['cleared_students']:
                print(f"  {student['student_id']}: Ksh.{student['total_paid']:,.2f}")
            
            print(f"\nPENDING STUDENTS ({len(report['pending_students'])}):")
            for student in report['pending_students']:
                print(f"  {student['student_id']}: Ksh.{student['total_paid']:,.2f} paid (Owes: Ksh.{student['amount_owed']:,.2f})")
                
        except ValueError as e:
            print(f"✗ Invalid input: {e}")
        except Exception as e:
            print(f"✗ Error generating report: {e}")
    
    def view_all_transactions(self):
        """View all transactions sorted by amount"""
        transactions = self.fee_tracker.get_sorted_transactions()
        if not transactions:
            print("No transactions recorded.")
            return
        
        total_revenue = self.fee_tracker.get_total_revenue()
        print(f"\n--- ALL TRANSACTIONS ({len(transactions)} total) ---")
        print(f"Total Revenue: Ksh.{total_revenue:,.2f}")
        print("\nTransactions (sorted by amount):")
        for tx in transactions:
            print(f"  Ksh.{tx.amount:>8,.2f} - {tx.student_id} - {tx.description}")
    
    def library_management_menu(self):
        """Library management submenu"""
        while True:
            print("\n--- LIBRARY MANAGEMENT ---")
            print("1. Add Book")
            print("2. Borrow Book")
            print("3. Return Book")
            print("4. Search Books")
            print("5. Book Status")
            print("6. Available Books")
            print("7. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.borrow_book()
            elif choice == '3':
                self.return_book()
            elif choice == '4':
                self.search_books()
            elif choice == '5':
                self.book_status()
            elif choice == '6':
                self.available_books()
            elif choice == '7':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def add_book(self):
        """Add a new book to library"""
        print("\n--- ADD BOOK ---")
        try:
            isbn = input("ISBN: ").strip()
            title = input("Title: ").strip()
            author = input("Author: ").strip()
            copies = int(input("Number of copies: ").strip())
            
            book = self.library_system.add_book(isbn, title, author, copies)
            print(f"✓ Book added: {book}")
            
        except ValueError as e:
            print(f"✗ Invalid input: {e}")
        except Exception as e:
            print(f"✗ Error adding book: {e}")
    
    def borrow_book(self):
        """Borrow a book"""
        print("\n--- BORROW BOOK ---")
        try:
            isbn = input("ISBN: ").strip()
            student_id = input("Student ID: ").strip()
            
            result = self.library_system.borrow_book(isbn, student_id)
            if result["success"]:
                print(f"✓ {result['message']}")
                print(f"  Available copies: {result['available_copies']}")
            else:
                print(f"✗ {result['message']}")
                
        except Exception as e:
            print(f"✗ Error borrowing book: {e}")
    
    def return_book(self):
        """Return a book"""
        print("\n--- RETURN BOOK ---")
        try:
            isbn = input("ISBN: ").strip()
            student_id = input("Student ID: ").strip()
            
            result = self.library_system.return_book(isbn, student_id)
            if result["success"]:
                print(f"✓ {result['message']}")
                print(f"  Available copies: {result['available_copies']}")
            else:
                print(f"✗ {result['message']}")
                
        except Exception as e:
            print(f"✗ Error returning book: {e}")
    
    def search_books(self):
        """Search books"""
        print("\n--- SEARCH BOOKS ---")
        title = input("Title search (leave empty for all): ").strip()
        author = input("Author search (leave empty for all): ").strip()
        
        books = self.library_system.search_books(title, author)
        if not books:
            print("No books found matching your criteria.")
            return
        
        print(f"\n--- SEARCH RESULTS ({len(books)} found) ---")
        for book in books:
            status = "Available" if book.available_copies > 0 else "Checked Out"
            print(f"{book.isbn}: {book.title} by {book.author} | {status} ({book.available_copies}/{book.total_copies})")
    
    def book_status(self):
        """Display book status"""
        print("\n--- BOOK STATUS ---")
        isbn = input("Enter ISBN: ").strip()
        
        status = self.library_system.get_book_status(isbn)
        if status:
            print(f"\nBook: {status['title']}")
            print(f"Author: {status['author']}")
            print(f"Copies: {status['available_copies']}/{status['total_copies']} available")
            print(f"Borrowed: {status['borrowed_copies']}")
            
            if status['recent_activity']:
                print("\nRecent Activity:")
                for activity in status['recent_activity']:
                    print(f"  {activity['student_id']} {activity['action']} on {activity['timestamp']}")
        else:
            print("✗ Book not found")
    
    def available_books(self):
        """List available books"""
        books = self.library_system.get_available_books()
        if not books:
            print("No books currently available.")
            return
        
        print(f"\n--- AVAILABLE BOOKS ({len(books)} total) ---")
        for book in books:
            print(f"{book.isbn}: {book.title} by {book.author} | {book.available_copies} available")
    
    def analytics_menu(self):
        """Analytics and reports submenu"""
        while True:
            print("\n--- ANALYTICS & REPORTS ---")
            print("1. Student Performance")
            print("2. Course Analytics")
            print("3. Top Performers")
            print("4. Student Ranking")
            print("5. Comprehensive Report")
            print("6. Back to Main Menu")
            
            choice = input("\nEnter your choice (1-6): ").strip()
            
            if choice == '1':
                self.student_performance()
            elif choice == '2':
                self.course_analytics()
            elif choice == '3':
                self.top_performers()
            elif choice == '4':
                self.student_ranking()
            elif choice == '5':
                self.comprehensive_report()
            elif choice == '6':
                break
            else:
                print("Invalid choice. Please try again.")
    
    def student_performance(self):
        """View student performance"""
        print("\n--- STUDENT PERFORMANCE ---")
        student_id = input("Student ID: ").strip()
        
        grades = self.analytics_engine.get_student_grades(student_id)
        if not grades:
            print("No grades recorded for this student.")
            return
        
        average = self.analytics_engine.get_student_average(student_id)
        ranking = self.analytics_engine.get_student_ranking(student_id)
        
        print(f"\nPerformance for {student_id}:")
        print(f"Overall Average: {average:.2f}%")
        if ranking:
            print(f"Rank: {ranking['rank']}/{ranking['total_students']}")
        
        print("\nCourse Grades:")
        for course_id, score in grades:
            print(f"  {course_id}: {score:.2f}%")
    
    def course_analytics(self):
        """View course analytics"""
        print("\n--- COURSE ANALYTICS ---")
        course_id = input("Course ID: ").strip()
        
        average = self.analytics_engine.get_course_average(course_id)
        top_students = self.analytics_engine.get_course_performance(course_id, 3)
        grades = self.analytics_engine.get_course_grades(course_id)
        
        if not grades:
            print("No grades recorded for this course.")
            return
        
        print(f"\nAnalytics for {course_id}:")
        print(f"Average Score: {average:.2f}%")
        print(f"Total Grades: {len(grades)}")
        
        if top_students:
            print("\nTop Performers:")
            for student in top_students:
                print(f"  {student['rank']}. {student['student_id']}: {student['score']:.2f}%")
    
    def top_performers(self):
        """Display top performers"""
        print("\n--- TOP PERFORMERS ---")
        try:
            n = int(input("Number of top performers to show (default 5): ").strip() or "5")
            top_performers = self.analytics_engine.get_top_performers(n)
            
            if not top_performers:
                print("No performance data available.")
                return
            
            print(f"\n🏆 TOP {len(top_performers)} PERFORMERS 🏆")
            for performer in top_performers:
                print(f"{performer['rank']}. {performer['student_id']}: {performer['average_score']:.2f}%")
                print(f"   Courses: {', '.join([f'{course}({score})' for course, score in performer['grades']])}")
                
        except ValueError:
            print("Invalid number entered.")
    
    def student_ranking(self):
        """Get student ranking"""
        print("\n--- STUDENT RANKING ---")
        student_id = input("Student ID: ").strip()
        
        ranking = self.analytics_engine.get_student_ranking(student_id)
        if ranking:
            print(f"\nRanking for {student_id}:")
            print(f"Position: {ranking['rank']} out of {ranking['total_students']} students")
            print(f"Average Score: {ranking['average_score']:.2f}%")
            
            # Calculate percentile
            percentile = (ranking['total_students'] - ranking['rank']) / ranking['total_students'] * 100
            print(f"Percentile: {percentile:.1f}%")
        else:
            print("No ranking data available for this student.")
    
    def comprehensive_report(self):
        """Generate comprehensive performance report"""
        print("\n--- COMPREHENSIVE PERFORMANCE REPORT ---")
        
        report = self.analytics_engine.generate_performance_report()
        
        print("\n" + "="*50)
        print("COMPREHENSIVE PERFORMANCE REPORT")
        print("="*50)
        print(f"Students with grades: {report['total_students_with_grades']}")
        print(f"Courses with grades: {report['total_courses_with_grades']}")
        print(f"Overall Average: {report['overall_average']:.2f}%")
        
        print(f"\n🏆 TOP 5 PERFORMERS:")
        for performer in report['top_performers']:
            print(f"  {performer['rank']}. {performer['student_id']}: {performer['average_score']:.2f}%")
        
        print(f"\n📊 COURSE STATISTICS:")
        for course_id, stats in report['course_statistics'].items():
            print(f"  {course_id}:")
            print(f"    Average: {stats['average_score']:.2f}%")
            print(f"    Total Grades: {stats['total_grades']}")
            if stats['top_students']:
                print(f"    Top Students: {', '.join([f'{s['student_id']}({s['score']:.1f}%)' for s in stats['top_students']])}")
    
    def run_demo(self):
        """Run a comprehensive system demo"""
        print("\n" + "="*60)
        print("🚀 SYSTEM DEMONSTRATION")
        print("="*60)
        
        # Initialize sample data
        initialize_sample_data(self)
        
        # Demonstrate key features
        print("\n=== DEMONSTRATING KEY FEATURES ===")
        
        # 1. Student Registry Demo
        print("\n1. STUDENT REGISTRY (Hash Table):")
        students = self.student_registry.get_all_students()
        print(f"   Total students: {len(students)}")
        if students:
            print(f"   Sample student: {students[0]}")
        
        # 2. Course Scheduling Demo
        print("\n2. COURSE SCHEDULING (Queue):")
        courses = self.course_scheduler.get_all_courses()
        print(f"   Total courses: {len(courses)}")
        if courses:
            cs101_status = self.course_scheduler.get_course_status("CS101")
            if cs101_status:
                print(f"   CS101: {cs101_status['enrolled_count']}/{cs101_status['capacity']} enrolled, {cs101_status['waitlist_count']} waitlisted")
        
        # 3. Fee Tracking Demo
        print("\n3. FEE TRACKING (BST):")
        print(f"   Total transactions: {len(self.fee_tracker)}")
        print(f"   Total revenue: ${self.fee_tracker.get_total_revenue():,.2f}")
        
        # Generate clearance report
        clearance_report = self.fee_tracker.generate_clearance_report(40000)
        print(f"   Fee clearance: {clearance_report['clearance_rate']:.1%}")
        
        # 4. Library System Demo
        print("\n4. LIBRARY SYSTEM (Stack):")
        print(f"   Total books: {len(self.library_system)}")
        available_books = self.library_system.get_available_books()
        print(f"   Available books: {len(available_books)}")
        
        # 5. Analytics Demo
        print("\n5. PERFORMANCE ANALYTICS (Heap):")
        top_performers = self.analytics_engine.get_top_performers(3)
        if top_performers:
            print(f"   Top performer: {top_performers[0]['student_id']} ({top_performers[0]['average_score']:.2f}%)")
        
        print("\n" + "="*60)
        print("✓ Demo completed successfully!")
        print("="*60)
    
    def run(self):
        """Main application loop"""
        print("Welcome to Meru University School Management System!")
        
        while True:
            self.display_menu()
            choice = input("\nEnter your choice (1-7): ").strip()
            
            if choice == '1':
                self.student_management_menu()
            elif choice == '2':
                self.course_management_menu()
            elif choice == '3':
                self.fee_management_menu()
            elif choice == '4':
                self.library_management_menu()
            elif choice == '5':
                self.analytics_menu()
            elif choice == '6':
                self.run_demo()
            elif choice == '7':
                print("\nThank you for using Meru University School Management System!")
                print("Goodbye! 👋")
                break
            else:
                print("Invalid choice. Please try again.")

def main():
    """Main entry point"""
    try:
        system = SchoolManagementSystem()
        system.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        print("Please check the system configuration and try again.")

if __name__ == "__main__":
    main()