import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.fee_tracker import FeeTracker

class TestFeeTracker(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        self.tracker = FeeTracker("data/test_transactions.json")
        # Clear any existing test data
        self.tracker.transactions.clear()
        self.tracker.root = None

    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists("data/test_transactions.json"):
            os.remove("data/test_transactions.json")

    def test_add_payment(self):
        """Test adding a payment"""
        transaction = self.tracker.add_payment("S001", 50000, "Tuition Fee")
        self.assertEqual(transaction.student_id, "S001")
        self.assertEqual(transaction.amount, 50000)
        self.assertEqual(transaction.description, "Tuition Fee")
        self.assertEqual(len(self.tracker), 1)

    def test_get_transaction(self):
        """Test retrieving transaction"""
        transaction = self.tracker.add_payment("S001", 50000, "Tuition Fee")
        retrieved = self.tracker.get_transaction(transaction.transaction_id)
        self.assertEqual(retrieved.transaction_id, transaction.transaction_id)
        self.assertEqual(retrieved.amount, 50000)

    def test_get_student_transactions(self):
        """Test getting transactions for a student"""
        self.tracker.add_payment("S001", 50000, "Tuition Fee")
        self.tracker.add_payment("S001", 5000, "Library Fee")
        self.tracker.add_payment("S002", 45000, "Tuition Fee")

        s001_transactions = self.tracker.get_student_transactions("S001")
        self.assertEqual(len(s001_transactions), 2)

        s002_transactions = self.tracker.get_student_transactions("S002")
        self.assertEqual(len(s002_transactions), 1)

    def test_sorted_transactions(self):
        """Test transaction sorting"""
        self.tracker.add_payment("S001", 30000, "Fee 1")
        self.tracker.add_payment("S002", 50000, "Fee 2")
        self.tracker.add_payment("S003", 40000, "Fee 3")

        sorted_tx = self.tracker.get_sorted_transactions()
        amounts = [tx.amount for tx in sorted_tx]
        self.assertEqual(amounts, [30000, 40000, 50000])  # Should be sorted ascending

    def test_clearance_report(self):
        """Test fee clearance report"""
        self.tracker.add_payment("S001", 45000, "Tuition")
        self.tracker.add_payment("S002", 35000, "Tuition")
        self.tracker.add_payment("S003", 50000, "Tuition")

        report = self.tracker.generate_clearance_report(40000)
        self.assertEqual(report["required_amount"], 40000)
        self.assertEqual(len(report["cleared_students"]), 2)  # S001 and S003
        self.assertEqual(len(report["pending_students"]), 1)  # S002

if __name__ == '__main__':
    unittest.main()
