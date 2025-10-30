import os
from models.transaction import Transaction
from utils.helpers import save_to_json, load_from_json, generate_id

class FeeTracker:
    def __init__(self, data_file="data/transactions.json"):
        self.root = None  # BST root
        self.transactions = {}  # Hash table for O(1) lookup: transaction_id -> Transaction
        self.data_file = data_file
        self._load_data()

    def _load_data(self):
        """Load transaction data from JSON file"""
        data = load_from_json(self.data_file)
        if data:
            for tx_data in data.values():
                try:
                    transaction = Transaction.from_dict(tx_data)
                    self.transactions[transaction.transaction_id] = transaction
                    # Rebuild BST
                    self.root = self._insert_bst(self.root, transaction)
                except Exception as e:
                    print(f"Error loading transaction {tx_data.get('transaction_id')}: {e}")
            print(f"✓ Loaded {len(self.transactions)} transactions from storage")

    def _save_data(self):
        """Save transaction data to JSON file"""
        data = {txid: tx.to_dict() for txid, tx in self.transactions.items()}
        if save_to_json(data, self.data_file):
            return True
        return False

    def _insert_bst(self, node, transaction):
        """Insert transaction into BST (sorted by amount)"""
        if node is None:
            return transaction

        if transaction.amount < node.amount:
            node.left = self._insert_bst(node.left, transaction)
        else:
            node.right = self._insert_bst(node.right, transaction)

        return node

    def add_payment(self, student_id, amount, description="Tuition Fee"):
        """Add a payment transaction"""
        try:
            # Generate unique transaction ID
            existing_ids = list(self.transactions.keys())
            transaction_id = generate_id("T", existing_ids)

            # Create transaction
            transaction = Transaction(transaction_id, student_id, amount, description)

            # Add to hash table for O(1) lookup
            self.transactions[transaction_id] = transaction

            # Add to BST for sorted reporting
            self.root = self._insert_bst(self.root, transaction)

            if self._save_data():
                return transaction
            else:
                # Rollback if save fails
                del self.transactions[transaction_id]
                self.root = self._rebuild_bst()  # Rebuild without the failed transaction
                raise Exception("Failed to save transaction data")

        except Exception as e:
            raise Exception(f"Failed to add payment: {e}")

    def _rebuild_bst(self):
        """Rebuild BST from transactions hash table"""
        root = None
        for transaction in self.transactions.values():
            root = self._insert_bst(root, transaction)
        return root

    def get_transaction(self, transaction_id):
        """Get transaction by ID - O(1) lookup"""
        return self.transactions.get(transaction_id)

    def get_student_transactions(self, student_id):
        """Get all transactions for a student"""
        return [tx for tx in self.transactions.values()
                if tx.student_id == student_id]

    def get_sorted_transactions(self):
        """Get all transactions sorted by amount (in-order traversal)"""
        transactions = []
        self._inorder_traversal(self.root, transactions)
        return transactions

    def _inorder_traversal(self, node, result):
        """In-order traversal of BST"""
        if node:
            self._inorder_traversal(node.left, result)
            result.append(node)
            self._inorder_traversal(node.right, result)

    def generate_clearance_report(self, required_amount):
        """Generate fee clearance report"""
        all_transactions = self.get_sorted_transactions()

        # Calculate total payments per student
        student_totals = {}
        for tx in all_transactions:
            if tx.student_id not in student_totals:
                student_totals[tx.student_id] = 0
            student_totals[tx.student_id] += tx.amount

        # Categorize students
        cleared = []
        pending = []

        for student_id, total_paid in student_totals.items():
            if total_paid >= required_amount:
                cleared.append({"student_id": student_id, "total_paid": total_paid})
            else:
                pending.append({
                    "student_id": student_id,
                    "total_paid": total_paid,
                    "amount_owed": required_amount - total_paid
                })

        return {
            "required_amount": required_amount,
            "cleared_students": cleared,
            "pending_students": pending,
            "clearance_rate": len(cleared) / len(student_totals) if student_totals else 0
        }

    def get_total_revenue(self):
        """Calculate total revenue from all transactions"""
        return sum(tx.amount for tx in self.transactions.values())

    def __str__(self):
        return f"FeeTracker({len(self.transactions)} transactions, Total: ${self.get_total_revenue():,.2f})"

    def __len__(self):
        return len(self.transactions)
