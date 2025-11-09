# School Management System - Design Document

**Course:** Data Structures and Algorithms  
**Institution:** Meru University  
**Team Members:** [Add your names here]  
**Date:** October 2025

---

## 1. Executive Summary

This document outlines the design and implementation of a modular School Management System for Meru University. The system uses five different data structures to efficiently handle student registration, course scheduling, fee tracking, library management, and performance analytics.

---

## 2. System Architecture Overview

### 2.1 System Components

The system consists of five independent modules that can interact through a central data repository (student records):

```

**Pseudocode:**

```python
FUNCTION borrow_book(isbn, student_id):
    # Step 1: Find book (O(1) hash lookup)
    book = books_catalog[isbn]
    IF book is NULL:
        RETURN Error("Book not found")
    
    # Step 2: Check availability
    IF book.available_copies <= 0:
        RETURN Error("No copies available")
    
    # Step 3: Update availability
    book.available_copies = book.available_copies - 1
    
    # Step 4: Create borrow record
    borrow_record = {
        "isbn": isbn,
        "student_id": student_id,
        "title": book.title,
        "borrow_date": CURRENT_DATE()
    }
    
    # Step 5: Push to stack (LIFO - O(1))
    borrowed_stack.PUSH(borrow_record)
    
    RETURN Success(borrow_record)
END FUNCTION

FUNCTION return_book():
    # Step 1: Check if any books borrowed
    IF borrowed_stack.IS_EMPTY():
        RETURN Error("No books to return")
    
    # Step 2: Pop most recent (LIFO - O(1))
    record = borrowed_stack.POP()
    
    # Step 3: Update book availability
    book = books_catalog[record.isbn]
    book.available_copies = book.available_copies + 1
    
    # Step 4: Return book info
    RETURN Success({
        "isbn": record.isbn,
        "title": record.title,
        "student_id": record.student_id,
        "return_date": CURRENT_DATE()
    })
END FUNCTION

# Time Complexity: O(1) for both operations
# Space Complexity: O(1) per transaction
```

---

### 5.5 Performance Analytics Flow

```
┌─────────────────────────────────────────────────┐
│     PERFORMANCE ANALYTICS (Heap-Based)          │
└─────────────────────────────────────────────────┘

    [START: Get top performers]
       ↓
    [Input: n (number of top students)]
       ↓
    ┌──────────────────────┐
    │ For each student,    │
    │ calculate average    │
    │ score across all     │
    │ subjects             │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Create (avg, id)     │
    │ pairs for all        │
    │ students             │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Build MAX-HEAP       │
    │ (Use negative values │
    │ for Python's min     │
    │ heap)                │
    └──────┬───────────────┘
           │
           ▼
        Heap Structure:
        
              95.5
             /    \
          87.5    80.0
          /  \    /
        75   82  78
           │
           ▼
    ┌──────────────────────┐
    │ Extract top N        │
    │ elements from heap   │
    │ (heappop N times)    │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Format results with  │
    │ rank, student_id,    │
    │ average, subjects    │
    └──────┬───────────────┘
           │
           ▼
    [Return top N performers]
           │
           ▼
        [END]
```

**Pseudocode:**

```python
FUNCTION add_score(student_id, subject, score):
    # Step 1: Initialize if new student
    IF student_id NOT IN scores_data:
        scores_data[student_id] = []
    
    # Step 2: Add score (O(1))
    scores_data[student_id].ADD({
        "subject": subject,
        "score": score,
        "date": CURRENT_DATE()
    })
    
    RETURN Success
END FUNCTION

FUNCTION get_top_performers(n):
    averages = []
    
    # Step 1: Calculate averages for all students (O(n × m))
    # where n = students, m = scores per student
    FOR EACH student_id IN scores_data:
        scores_list = scores_data[student_id]
        
        IF LENGTH(scores_list) == 0:
            CONTINUE
        
        # Calculate average
        total = 0
        FOR EACH score_record IN scores_list:
            total = total + score_record.score
        END FOR
        
        average = total / LENGTH(scores_list)
        
        # Step 2: Add to heap (O(log n))
        # Use negative for max-heap behavior
        heappush(averages, (-average, student_id, scores_list))
    END FOR
    
    # Step 3: Extract top n elements (O(k log n))
    top_performers = []
    FOR i FROM 1 TO n:
        IF averages is EMPTY:
            BREAK
        
        neg_avg, student_id, scores = heappop(averages)
        actual_avg = -neg_avg
        
        top_performers.ADD({
            "rank": i,
            "student_id": student_id,
            "average": actual_avg,
            "scores": scores
        })
    END FOR
    
    RETURN top_performers
END FUNCTION

# Time Complexity Analysis:
# - Calculate averages: O(n × m) where m = avg scores per student
# - Build heap: O(n)
# - Extract top k: O(k log n)
# Total: O(n × m + k log n) ≈ O(n) for small m and k

# Space Complexity: O(n) for heap storage
```

---

### 5.6 Complete System Integration Flow

```
┌─────────────────────────────────────────────────────────┐
│         COMPLETE STUDENT LIFECYCLE FLOW                 │
└─────────────────────────────────────────────────────────┘

[1. REGISTRATION]
       ↓
   Student Data
   → Hash Table
       ↓
[2. ENROLLMENT]
       ↓
   Course Queue
   (FIFO Logic)
       ↓
   ┌────────┐
   │Enrolled│
   └───┬────┘
       ↓
[3. FEE PAYMENT]
       ↓
   Transaction
   → BST (sorted)
   → Hash (quick lookup)
       ↓
   ┌────────┐
   │Cleared?│
   └───┬────┘
       ↓
[4. LIBRARY ACCESS]
       ↓
   Borrow Books
   → Stack (LIFO)
       ↓
[5. ACADEMICS]
       ↓
   Submit Scores
   → Heap Analysis
       ↓
   Generate Rankings
       ↓
[6. GRADUATION]
       ↓
   Remove from
   Hash Table
       ↓
    [END]
```

**Complete Integration Pseudocode:**

```python
FUNCTION process_new_student(name, email, year):
    # Step 1: Register student
    student_id = GENERATE_ID()
    student = student_registry.add_student(student_id, name, email, year)
    
    # Step 2: Enroll in courses
    desired_courses = GET_STUDENT_COURSE_PREFERENCES()
    FOR EACH course_id IN desired_courses:
        result = course_scheduler.enroll_student(course_id, student_id)
        
        IF result.status == "waitlisted":
            NOTIFY(student, "Added to waitlist position: " + result.position)
        END IF
    END FOR
    
    # Step 3: Record fee payment
    payment_amount = GET_PAYMENT_FROM_STUDENT()
    transaction = fee_tracker.add_payment(
        student_id, 
        payment_amount, 
        "Initial semester fees"
    )
    
    # Step 4: Check clearance
    clearance = fee_tracker.generate_clearance_report(REQUIRED_FEE)
    IF student_id IN clearance.cleared:
        GRANT_LIBRARY_ACCESS(student_id)
    ELSE:
        RESTRICT_LIBRARY_ACCESS(student_id)
    END IF
    
    # Step 5: Throughout semester - record academic performance
    # (This happens over time as exams/assignments are graded)
    
    # Step 6: At end of semester - generate performance report
    analytics.add_score(student_id, "Math", 85)
    analytics.add_score(student_id, "Physics", 90)
    # ... more scores
    
    top_students = analytics.get_top_performers(10)
    
    RETURN {
        "student": student,
        "enrollment_status": "Active",
        "fee_status": "Cleared" OR "Pending",
        "academic_standing": DETERMINE_FROM_SCORES()
    }
END FUNCTION

# This demonstrates how all 5 data structures work together
# to manage a student's complete academic lifecycle
```

---

## 6. System Requirements
```
 ─────────────────────────────────────────────────┐
│         SCHOOL MANAGEMENT SYSTEM                │
├─────────────────────────────────────────────────┤
│                                                 │
│  ┌──────────────┐      ┌──────────────┐         │
│  │   Student    │      │   Course     │         │
│  │   Registry   │◄────►│  Scheduler   │         │
│  │ (Hash Table) │      │   (Queue)    │         │
│  └──────────────┘      └──────────────┘         │
│         ▲                      ▲                │
│         │                      │                │
│         ▼                      ▼                │
│  ┌──────────────┐      ┌──────────────┐         │
│  │     Fee      │      │   Library    │         │
│  │   Tracker    │      │   System     │         │
│  │    (BST)     │      │   (Stack)    │         │
│  └──────────────┘      └──────────────┘         │
│                                                 │
│         ┌──────────────────────┐                │
│         │   Performance        │                │
│         │   Analytics (Heap)   │                │
│         └──────────────────────┘                │
└─────────────────────────────────────────────────┘
```

### 2.2 Data Flow

1. **Student Registration** → Student added to hash table
2. **Course Enrollment** → Student ID retrieved from registry, added to course queue
3. **Fee Payment** → Payment recorded in BST, linked to student ID
4. **Library Transaction** → Student borrows/returns books via stack
5. **Performance Tracking** → Scores recorded and analyzed using heap

---

## 3. Module Design & Data Structure Justification

### 3.1 Student Registry - Hash Table (Dictionary)

**Purpose:** Store and retrieve student information quickly.

**Why Hash Table?**
- **O(1) average time complexity** for add, search, and delete operations
- Student ID serves as a unique key (no collisions in our implementation)
- Perfect for frequent lookups when enrolling courses or tracking fees
- Python's built-in `dict` provides efficient hash table implementation

**Key Operations:**
```python
add_student(id, name, email)     # O(1)
find_student(id)                 # O(1)
remove_student(id)               # O(1)
```

**Trade-offs:**
- ✅ Extremely fast lookup
- ✅ Simple implementation
- ❌ No inherent ordering (but we don't need it here)
- ❌ Higher memory usage than arrays

---

### 3.2 Course Scheduling - Queue (FIFO)

**Purpose:** Manage course enrollment and waitlists fairly.

**Why Queue?**
- **First-In-First-Out (FIFO)** ensures fairness - students who register first get priority
- O(1) for enqueue (add to waitlist) and dequeue (enroll from waitlist)
- Models real-world course registration accurately
- Used Python's `collections.deque` for efficient operations at both ends

**Key Operations:**
```python
enroll_student(course, student)   # O(1) - add to queue
process_waitlist(course)          # O(1) - remove from queue
```

**Trade-offs:**
- ✅ Fair allocation (first-come, first-served)
- ✅ Efficient operations
- ❌ Cannot prioritize students (e.g., seniors first) without modifying structure

**Alternative Considered:** Priority Queue - rejected because fairness by time is more important than priority by year/grade.

---

### 3.3 Fee Tracking - Binary Search Tree (BST)

**Purpose:** Maintain sorted fee records and generate reports efficiently.

**Why Binary Search Tree?**
- Maintains data in **sorted order** (by payment amount)
- O(log n) average insertion and search
- Easy to generate sorted reports via in-order traversal
- Can quickly find students who paid above/below threshold

**Key Operations:**
```python
add_payment(student_id, amount)   # O(log n) average
get_sorted_payments()             # O(n) - in-order traversal
generate_clearance_report()       # O(n)
```

**Tree Structure Example:**
```
        50000 (S001)
       /            \
   35000 (S002)   50000 (S003)
```

**Trade-offs:**
- ✅ Sorted output for reports
- ✅ Efficient range queries (find all payments between X and Y)
- ❌ Can degrade to O(n) if unbalanced (solution: use AVL tree)
- ❌ Slower than hash table for simple lookups

**Alternative Considered:** Hash Table - faster lookup but no sorted reports. BST chosen because fee clearance reports need sorted data.

---

### 3.4 Library System - Stack (LIFO)

**Purpose:** Track book borrowing and returns with recent transaction priority.

**Why Stack?**
- **Last-In-First-Out (LIFO)** - most recent transactions are processed first
- O(1) for push (borrow) and pop (return)
- Simple to implement and understand
- Efficient for tracking transaction history

**Key Operations:**
```python
borrow_book(isbn, student)    # O(1) - push to stack
return_book()                 # O(1) - pop from stack
display_borrowed()            # O(n) - view all
```

**Stack Visualization:**
```
TOP → [ISBN001, S002, "Algorithms"]  ← Most recent
      [ISBN001, S001, "Algorithms"]  ← Older
```

**Trade-offs:**
- ✅ Very efficient operations
- ✅ Easy to see recent activity
- ❌ Returns must be in reverse order (can be modified if needed)
- ❌ Cannot search middle of stack efficiently

**Alternative Considered:** Queue - but LIFO better represents "undo" pattern in library returns.

---

### 3.5 Performance Analytics - Heap (Priority Queue)

**Purpose:** Identify top-performing students efficiently.

**Why Heap?**
- O(log n) insertion, O(1) for finding max/min
- Perfect for **finding top K elements** (top performers)
- More efficient than sorting entire dataset
- Python's `heapq` module provides min-heap (we use negative values for max-heap)

**Key Operations:**
```python
add_score(student, subject, score)  # O(log n)
get_top_performers(n)               # O(n log k)
```

**Heap Structure (Max Heap - Top Averages):**
```
          95.5 (S003)
         /           \
    87.5 (S001)    80.0 (S002)
```

**Trade-offs:**
- ✅ Efficient for finding top K students
- ✅ Doesn't require sorting all students
- ❌ Extracting all elements in order is O(n log n)
- ❌ Cannot efficiently search for arbitrary student

**Alternative Considered:** Simple sorting - O(n log n) every time. Heap is better when we only need top performers.

---

## 4. System Workflow Examples

### Example 1: Student Enrollment Process

```
1. Student registers → Added to Hash Table (O(1))
2. Student enrolls in course → 
   - Check capacity
   - If full: Add to Queue (O(1))
   - If available: Enroll directly
3. Student pays fees → Added to BST (O(log n))
4. Fee clearance checked → BST traversal (O(n))
```

### Example 2: Library Transaction

```
1. Student borrows book → 
   - Check availability in Hash Table (O(1))
   - Push transaction to Stack (O(1))
2. Student returns book → 
   - Pop from Stack (O(1))
   - Update availability
```

---

## 5. Detailed Flow Diagrams with Pseudocode

### 5.1 Student Registration Flow

```
┌─────────────────────────────────────────────────┐
│         STUDENT REGISTRATION FLOW               │
└─────────────────────────────────────────────────┘

    [START]
       ↓
    [Input: student_id, name, email, year]
       ↓
    ┌──────────────────────┐
    │ Check if ID exists   │
    │ in hash table        │
    └──────┬───────────────┘
           │
    ┌──────▼──────┐
    │ ID exists?  │
    └──────┬──────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
 [Return     [Create Student
  Error]      Object]
              │
              ▼
         [Calculate hash
          from ID]
              │
              ▼
         [Insert into
          hash_table[ID]]
              │
              ▼
         [Return Success
          + Student obj]
              │
              ▼
           [END]
```

**Pseudocode:**

```python
FUNCTION add_student(student_id, name, email, year):
    # Step 1: Validate input
    IF student_id is empty OR name is empty:
        RETURN Error("Invalid input")
    
    # Step 2: Check for duplicate (Hash Table Lookup - O(1))
    hash_key = HASH(student_id)
    IF hash_table[hash_key] exists:
        RETURN Error("Student already exists")
    
    # Step 3: Create student object
    student = NEW Student(student_id, name, email, year)
    student.courses = []
    student.fees_paid = 0
    
    # Step 4: Insert into hash table (O(1))
    hash_table[hash_key] = student
    
    # Step 5: Return success
    RETURN Success(student)
END FUNCTION

# Time Complexity: O(1) average
# Space Complexity: O(1) for single student
```

---

### 5.2 Course Enrollment Flow

```
┌─────────────────────────────────────────────────┐
│          COURSE ENROLLMENT FLOW                 │
└─────────────────────────────────────────────────┘

    [START: Student requests enrollment]
       ↓
    [Input: course_id, student_id]
       ↓
    ┌──────────────────────┐
    │ Lookup course by ID  │
    │ (Hash Table - O(1))  │
    └──────┬───────────────┘
           │
    ┌──────▼──────┐
    │ Course      │
    │ exists?     │
    └──────┬──────┘
           │
     ┌─────┴─────┐
     │           │
    NO          YES
     │           │
     ▼           ▼
 [Return    ┌─────────────────┐
  Error]    │ Check if student│
            │ already enrolled│
            └────────┬────────┘
                     │
              ┌──────▼──────┐
              │ Already     │
              │ enrolled?   │
              └──────┬──────┘
                     │
               ┌─────┴─────┐
               │           │
              YES         NO
               │           │
               ▼           ▼
           [Return    ┌──────────────┐
            Status:   │ Check if     │
            Already   │ course full  │
            Enrolled] └──────┬───────┘
                             │
                      ┌──────▼──────┐
                      │ Capacity    │
                      │ available?  │
                      └──────┬──────┘
                             │
                       ┌─────┴─────┐
                       │           │
                      YES         NO
                       │           │
                       ▼           ▼
                  [Add to      [Add to
                   enrolled    waitlist
                   list]       queue - FIFO]
                       │           │
                       ▼           ▼
                  [Return     [Return
                   Status:     Status:
                   Enrolled]   Waitlisted
                               Position: N]
                       │           │
                       └─────┬─────┘
                             ▼
                          [END]
```

**Pseudocode:**

```python
FUNCTION enroll_student(course_id, student_id):
    # Step 1: Find course (Hash Table - O(1))
    course = courses_table[course_id]
    IF course is NULL:
        RETURN Error("Course not found")
    
    # Step 2: Check if already enrolled (O(1) with hash set)
    IF student_id IN course.enrolled_students:
        RETURN {"status": "already_enrolled", "position": 0}
    
    # Step 3: Check capacity
    IF LENGTH(course.enrolled_students) < course.capacity:
        # Step 3a: Direct enrollment
        course.enrolled_students.ADD(student_id)
        student = students_table[student_id]
        student.courses.ADD(course_id)
        RETURN {"status": "enrolled", "position": 0}
    ELSE:
        # Step 3b: Add to waitlist (Queue - O(1))
        course.waitlist.ENQUEUE(student_id)
        position = LENGTH(course.waitlist)
        RETURN {"status": "waitlisted", "position": position}
    END IF
END FUNCTION

# Time Complexity: O(1) for all operations
# Space Complexity: O(1) per enrollment
```

**Waitlist Processing:**

```python
FUNCTION process_waitlist(course_id):
    course = courses_table[course_id]
    IF course is NULL:
        RETURN []
    
    newly_enrolled = []
    
    # Process while there are spots and students waiting
    WHILE course.waitlist is NOT empty AND 
          LENGTH(course.enrolled_students) < course.capacity:
        
        # FIFO - First person in waitlist gets the spot
        student_id = course.waitlist.DEQUEUE()  # O(1)
        course.enrolled_students.ADD(student_id)
        newly_enrolled.ADD(student_id)
        
        # Notify student (in real system)
        SEND_NOTIFICATION(student_id, "You've been enrolled!")
    END WHILE
    
    RETURN newly_enrolled
END FUNCTION

# Time Complexity: O(k) where k = spots available
```

---

### 5.3 Fee Payment and Tracking Flow

```
┌─────────────────────────────────────────────────┐
│          FEE PAYMENT & BST INSERTION            │
└─────────────────────────────────────────────────┘

    [START: Payment received]
       ↓
    [Input: student_id, amount, description]
       ↓
    ┌──────────────────────┐
    │ Generate transaction │
    │ ID (T0001, T0002...) │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Create Transaction   │
    │ object with timestamp│
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Add to hash table    │
    │ for quick lookup     │
    │ (O(1))               │
    └──────┬───────────────┘
           │
           ▼
    ┌──────────────────────┐
    │ Insert into BST      │
    │ (sorted by amount)   │
    └──────┬───────────────┘
           │
           ▼
    [BST Insert Logic - Detailed Below]
           │
           ▼
    ┌──────────────────────┐
    │ Update student's     │
    │ total fees_paid      │
    └──────┬───────────────┘
           │
           ▼
    [Return Transaction object]
           │
           ▼
        [END]

┌─────────────────────────────────────────────────┐
│         BST INSERTION (Detailed)                │
└─────────────────────────────────────────────────┘

    [Start with root node]
           │
           ▼
    ┌──────────────┐
    │ Root is NULL?│
    └──────┬───────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
 [New node   [Compare amount
  becomes     with current
  root]       node amount]
     │           │
     └─────┬─────┘
           │
     ┌─────▼─────────┐
     │ New amount <  │
     │ Current amount│
     └─────┬─────────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
 [Recursively [Recursively
  insert to    insert to
  LEFT child]  RIGHT child]
     │           │
     └─────┬─────┘
           ▼
    [Update parent
     pointers]
           │
           ▼
        [END]
```

**Pseudocode:**

```python
FUNCTION add_payment(student_id, amount, description):
    # Step 1: Generate unique transaction ID
    transaction_count = transaction_count + 1
    transaction_id = "T" + PAD(transaction_count, 4)
    
    # Step 2: Create transaction object
    transaction = NEW Transaction(
        id = transaction_id,
        student_id = student_id,
        amount = amount,
        description = description,
        timestamp = CURRENT_TIME()
    )
    
    # Step 3: Add to hash table for O(1) lookup
    transactions_table[transaction_id] = transaction
    
    # Step 4: Insert into BST for sorted reports (O(log n))
    root = insert_into_bst(root, transaction)
    
    # Step 5: Update student's total fees
    student = students_table[student_id]
    student.fees_paid = student.fees_paid + amount
    
    RETURN transaction
END FUNCTION

# BST Insertion Function
FUNCTION insert_into_bst(node, transaction):
    # Base case: Empty spot found
    IF node is NULL:
        RETURN NEW BSTNode(transaction)
    
    # Recursive case: Navigate tree
    IF transaction.amount < node.transaction.amount:
        # Go left (smaller amounts)
        node.left = insert_into_bst(node.left, transaction)
    ELSE:
        # Go right (larger or equal amounts)
        node.right = insert_into_bst(node.right, transaction)
    END IF
    
    RETURN node
END FUNCTION

# Time Complexity: O(log n) average, O(n) worst case
# Space Complexity: O(1) for insertion, O(log n) recursion stack
```

**Fee Clearance Report Generation:**

```python
FUNCTION generate_clearance_report(required_amount):
    cleared = []
    pending = []
    
    # Traverse all transactions (O(n))
    FOR EACH transaction IN transactions_table.values():
        IF transaction.amount >= required_amount:
            cleared.ADD(transaction)
        ELSE:
            owed = required_amount - transaction.amount
            pending.ADD({
                "transaction": transaction,
                "amount_owed": owed
            })
        END IF
    END FOR
    
    RETURN {
        "cleared": cleared,
        "pending": pending,
        "required_amount": required_amount,
        "total_cleared": LENGTH(cleared),
        "total_pending": LENGTH(pending)
    }
END FUNCTION

# Time Complexity: O(n) where n = number of transactions
```

---

### 5.4 Library Book Management Flow

```
┌─────────────────────────────────────────────────┐
│        LIBRARY BORROWING (Stack-Based)          │
└─────────────────────────────────────────────────┘

    [START: Student wants to borrow]
       ↓
    [Input: isbn, student_id]
       ↓
    ┌──────────────────────┐
    │ Lookup book by ISBN  │
    │ (Hash Table - O(1))  │
    └──────┬───────────────┘
           │
    ┌──────▼──────┐
    │ Book exists?│
    └──────┬──────┘
           │
     ┌─────┴─────┐
     │           │
    NO          YES
     │           │
     ▼           ▼
 [Return    ┌──────────────┐
  Error:    │ Check if     │
  Not       │ copies       │
  Found]    │ available    │
            └──────┬───────┘
                   │
            ┌──────▼──────┐
            │ Available > 0│
            └──────┬───────┘
                   │
             ┌─────┴─────┐
             │           │
            YES         NO
             │           │
             ▼           ▼
        [Decrease    [Return
         available    Error:
         count]       No copies]
             │
             ▼
        ┌─────────────────┐
        │ Create borrow   │
        │ record (isbn,   │
        │ student_id,     │
        │ title)          │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │ PUSH to stack   │
        │ (O(1))          │
        │ [Most recent on │
        │  top]           │
        └────────┬────────┘
                 │
                 ▼
        [Return Success]
                 │
                 ▼
              [END]

┌─────────────────────────────────────────────────┐
│        LIBRARY RETURN (Stack Pop)               │
└─────────────────────────────────────────────────┘

    [START: Return book]
       ↓
    ┌──────────────┐
    │ Stack empty? │
    └──────┬───────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
 [Return    [POP from stack
  Error:     (O(1))]
  No         │
  books]     ▼
         [Get: isbn,
          student_id,
          title]
             │
             ▼
         [Increase
          available
          count]
             │
             ▼
         [Return
          Success +
          book info]
             │
             ▼
          [END]
```

**Pseudocode:**

```python
FUNCTION borrow_book(isbn, student_id):
    # Step 1: Find book (O(1) hash lookup)
    book = books_catalog[isbn]
    IF book is NULL:
        RETURN Error("Book not found")
    
    # Step 2: Check availability
    IF book.available_copies <= 0:
        RETURN Error("No copies available")
    
    # Step 3: Update availability
    book.available_copies = book.available_copies - 1
    
    # Step 4: Create borrow record
    borrow_record = {
        "isbn": isbn,
        "student_id": student_id,
        "title": book.title,
        "borrow_date": CURRENT_DATE()
    }
    
    # Step 5: Push to stack (LIFO - O(1))
    borrowed_stack.PUSH(borrow_record)
    
    RETURN Success(borrow_record)
END FUNCTION

FUNCTION return_book():
    # Step 1: Check if any books borrowed
    IF borrowed_stack.IS_EMPTY():
        RETURN Error("No books to return")
    
    # Step 2: Pop most recent (LIFO - O(1))
    record = borrowed_stack.POP()
    
    # Step 3: Update book availability
    book = books_catalog[record.isbn]
    book.available_copies = book.available_copies + 1
    
    # Step 4: Return book info
    RETURN Success({
        "isbn": record.isbn,
        "title": record.title,
        "student_id": record.student_id,
        "return_date": CURRENT_DATE()
    })
END FUNCTION

# Time Complexity: O(1) for both operations
# Space Complexity: O(1) per transaction
```

---

### 5.5 Performance Analytics Flow

```
┌

### Student Registration (Hash Table)

```
FUNCTION add_student(student_id, name, email):
    IF student_id EXISTS in hash_table:
        RETURN "Student already exists"
    
    hash_table[student_id] = {
        name: name,
        email: email,
        courses: [],
        fees_paid: 0
    }
    
    RETURN "Student added successfully"
```

### Course Enrollment (Queue)

```
FUNCTION enroll_student(course_name, student_id):
    course = get_course(course_name)
    
    IF student_id IN course.enrolled:
        RETURN "Already enrolled"
    
    IF course.enrolled.size < course.capacity:
        course.enrolled.ADD(student_id)
        RETURN "Enrolled successfully"
    ELSE:
        course.queue.ENQUEUE(student_id)
        RETURN "Added to waitlist"
```

### Fee Payment (BST)

```
FUNCTION insert_payment(root, student_id, amount):
    IF root IS NULL:
        RETURN new Node(student_id, amount)
    
    IF amount < root.amount:
        root.left = insert_payment(root.left, student_id, amount)
    ELSE:
        root.right = insert_payment(root.right, student_id, amount)
    
    RETURN root
```

---

## 6. System Requirements

### Functional Requirements:
- ✅ Add, search, and remove students
- ✅ Enroll students in courses with waitlist management
- ✅ Record and track fee payments
- ✅ Manage library book borrowing/returns
- ✅ Generate performance reports

### Non-Functional Requirements:
- **Performance:** All critical operations < O(n)
- **Scalability:** Support 1000+ students
- **Usability:** Clear command-line interface
- **Maintainability:** Modular design, well-commented code

---

## 7. Future Enhancements

1. **Persistent Storage:** Save data to database instead of memory
2. **GUI Interface:** Web-based dashboard for administrators
3. **Advanced Search:** Multi-criteria student search (by name, course, etc.)
4. **Email Notifications:** Auto-notify students when enrolled from waitlist
5. **AVL Tree:** Replace BST with self-balancing AVL tree for guaranteed O(log n)

---

## 8. Conclusion

This system demonstrates practical application of five fundamental data structures to solve real-world university management problems. Each structure was chosen based on the specific operational requirements of its module, balancing performance, simplicity, and maintainability.

The modular design allows independent development and testing of each component while maintaining system cohesion through shared student data. The implementation prioritizes efficiency for frequent operations while maintaining code readability and extensibility.

---

**Document Version:** 1.0  
**Last Updated:** October 2025
