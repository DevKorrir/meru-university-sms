# 🏫 Meru University School Management System

A modular School Management System implemented in Python that demonstrates the practical application of five fundamental data structures to solve real-world educational administration problems.

## 📋 Project Overview

This system was developed as part of the Data Structures and Algorithms course to modernize Meru University's internal systems. The prototype efficiently handles student registration, course scheduling, fee tracking, library management, and performance analytics using optimized data structures.

## 🚀 Key Features

### ✅ Enhanced Functionality
- **Student Management**: Complete CRUD operations with validation
- **Course Enrollment**: FIFO waitlist system with automatic processing
- **Fee Tracking**: BST-powered sorted reports and clearance tracking
- **Library Management**: LIFO book borrowing with activity history
- **Performance Analytics**: Heap-based ranking and comprehensive reporting
- **Data Persistence**: Automatic JSON file storage
- **Error Handling**: Comprehensive input validation and exception handling

## 🏗️ System Architecture

### Project Structure
```
school_management/
│
├── models/           # Data models with validation
│   ├── __init__.py
│   ├── student.py    # Student class with email/year validation
│   ├── course.py     # Course class with queue-based waitlist
│   ├── book.py       # Book class with borrow history
│   └── transaction.py # Transaction class for BST operations
│
├── services/         # Business logic with data structures
│   ├── __init__.py
│   ├── student_registry.py      # Hash Table - O(1) operations
│   ├── course_scheduler.py      # Queue - FIFO enrollment
│   ├── fee_tracker.py           # BST + Hash Table - O(log n) + O(1)
│   ├── library_system.py        # Stack - LIFO transactions
│   └── analytics_engine.py      # Heap - Top performers ranking
│
├── utils/            # Helper functions and validation
│   ├── __init__.py
│   ├── helpers.py    # JSON persistence, ID generation
│   └── validators.py # Email, ISBN, date validation
│
├── data/             # Automatic JSON persistence
│   ├── __init__.py
│   ├── sample_data.py # Comprehensive sample data
│   ├── students.json
│   ├── courses.json
│   ├── transactions.json
│   └── books.json
│
├── tests/            # Comprehensive unit tests
│   ├── __init__.py
│   ├── test_student_registry.py
│   ├── test_course_scheduler.py
│   ├── test_fee_tracker.py
│   ├── test_library_system.py
│   └── test_analytics_engine.py
│
├── main.py           # Interactive menu system
├── requirements.txt  # No external dependencies
└── README.md
```

### Core Modules & Data Structures

| Module | Data Structure | Key Operations | Time Complexity |
|--------|----------------|----------------|-----------------|
| Student Registry | Hash Table | Insert, Lookup, Delete | O(1) average |
| Course Scheduling | Queue (FIFO) | Enqueue, Dequeue | O(1) |
| Fee Tracking | Binary Search Tree | Insert, Range Query, In-order Traversal | O(log n) |
| Library System | Stack (LIFO) | Push, Pop, Lookup | O(1) |
| Performance Analytics | Heap (Priority Queue) | Add Edge, Traverse, Analyze | O(log n) |

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- No external dependencies required

### Quick Start
```bash
# Clone the repository
git clone https://github.com/DevKorrir/meru-university-sms.git
cd school-management-system

# Run the system (no installation required)
python main.py

# Run comprehensive tests
python -m unittest discover tests

# Run specific module tests
python -m unittest tests.test_student_registry
```

### 🎯 Usage Examples

```python
# The system provides an interactive menu, but you can also use it programmatically:
from services.student_registry import StudentRegistry
from services.course_scheduler import CourseScheduler

# Initialize modules
registry = StudentRegistry()
scheduler = CourseScheduler()

# Add student with automatic validation
student = registry.add_student("S001", "John Doe", "john@meru.edu", 2)

# Create course and enroll students
course = scheduler.create_course("CS101", "Data Structures", 30)
result = scheduler.enroll_student("CS101", "S001")
```

## 📊 Performance Characteristics

| Operation | Data Structure | Time Complexity | Space Complexity | Features |
|-----------|----------------|-----------------|------------------|----------|
| Student Lookup | Hash Table | O(1) average | O(n) | Email validation, auto-persistence |
| Course Enrollment | Queue | O(1) | O(n) | Waitlist fairness, capacity management |
| Payment Sorting | BST | O(log n) | O(n) | Sorted reports, clearance tracking |
| Book Return | Stack | O(1) | O(n) | Activity history, availability tracking |
| Top Performers | Heap | O(log n) | O(n) | Ranking system, course analytics |

## 🧪 Testing

The system includes comprehensive unit tests:

```bash
# Run all tests
python -m unittest discover tests

# Run specific test modules
python -m unittest tests.test_student_registry
python -m unittest tests.test_course_scheduler
python -m unittest tests.test_fee_tracker
python -m unittest tests.test_library_system
python -m unittest tests.test_analytics_engine

# Test coverage includes:
# - Data structure operations
# - Error handling and validation
# - Data persistence
# - Edge cases and boundary conditions
```

## 🔧 Advanced Features

### Data Persistence
- **Automatic JSON serialization** for all modules
- **Data integrity** with validation and error recovery
- **Sample data initialization** for demonstration

### Error Handling
- **Input validation** for emails, IDs, amounts, dates
- **Comprehensive exception handling** with user-friendly messages
- **Data consistency** with rollback mechanisms

### Modular Design
- **Separation of concerns** with models, services, and utils
- **Team-friendly** structure for collaborative development
- **Extensible architecture** for adding new features

## 📈 System Demo

Run the built-in demonstration to see all features in action:

```bash
python main.py
# Then select option 6: "System Demo"
```

The demo will:
1. Initialize sample data (students, courses, transactions, books, grades)
2. Demonstrate all 5 data structures in action
3. Show real-world usage scenarios
4. Generate comprehensive reports

## 🤝 Contributing

This is a group project for educational purposes. For contributions:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add some improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guide
- Write unit tests for new features
- Update documentation accordingly
- Use descriptive commit messages


## 📄 License

This project is for educational purposes as part of Meru University's Data Structures and Algorithms course.

## 👥 Team Members
- Aldo Kipyegon Korir
- Wambui Samuel Mwangi
- Mwanik Paul Kibe
- Omwoyo Miriam Bwari

## 📚 Course Information
- **Course**: Data Structures and Algorithms
- **Instructor**: Dismas Kitaria
- **Semester**: Sem1-2025/2026
- **Due Date**: */10/2025

## 🎯 Learning Outcomes

This project demonstrates:
- **Practical application** of 5 fundamental data structures
- **Software engineering best practices** (modularity, testing, documentation)
- **Real-world problem solving** in educational administration
- **Team collaboration** and version control proficiency
- **Algorithm analysis** and complexity optimization

---

**⭐ If you find this project helpful, please give it a star!**

---

Made with ❤️ by Group two at Meru University
