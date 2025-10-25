# 🏫 Meru University School Management System

A modular School Management System implemented in Python that demonstrates the practical application of five fundamental data structures to solve real-world educational administration problems.

## 📋 Project Overview

This system was developed as part of the Data Structures and Algorithms course to modernize Meru University's internal systems. The prototype efficiently handles student registration, course scheduling, fee tracking, library management, and performance analytics using optimized data structures.

## 🏗️ System Architecture

### Project Structure
```
school_management/
│
├── models/           # Data models
│   ├── __init__.py
│   ├── student.py
│   ├── course.py
│   ├── book.py
│   └── transaction.py
│
├── services/         # Business logic with data structures
│   ├── __init__.py
│   ├── student_registry.py      # Hash Table
│   ├── course_scheduler.py      # Queue  
│   ├── fee_tracker.py           # BST
│   ├── library_system.py        # Stack
│   └── analytics_engine.py      # Heap/Graph
│
├── utils/            # Helper functions
│   ├── __init__.py
│   └── helpers.py
│
├── data/             # Data storage
│   ├── students.json
│   ├── courses.json
│   └── transactions.json
│
├── tests/            # Unit tests
│   ├── __init__.py
│   ├── test_student_registry.py
│   └── test_course_scheduler.py
│
├── main.py           # Entry point
├── requirements.txt
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

# Run the system
python main.py
```































## 🤝 Contributing

This is a group project for educational purposes. For contributions:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Submit a pull request

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
```
