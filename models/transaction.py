from utils.validators import validate_amount, validate_date

class Transaction:
    def __init__(self, transaction_id, student_id, amount, description="", date=None):
        self.transaction_id = transaction_id
        self.student_id = student_id
        self.amount = amount
        self.description = description
        self.date = date or self._get_current_date()
        self.left = None
        self.right = None

        self._validate_inputs()

    def _validate_inputs(self):
        """Validate transaction data"""
        if not self.transaction_id or not isinstance(self.transaction_id, str):
            raise ValueError("Transaction ID must be a non-empty string")

        if not self.student_id or not isinstance(self.student_id, str):
            raise ValueError("Student ID must be a non-empty string")

        if not validate_amount(self.amount):
            raise ValueError("Amount must be a positive number")

        if not validate_date(self.date):
            raise ValueError("Invalid date format")

    def _get_current_date(self):
        """Get current date (simplified)"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")

    def to_dict(self):
        """Convert transaction to dictionary for JSON serialization"""
        return {
            'transaction_id': self.transaction_id,
            'student_id': self.student_id,
            'amount': self.amount,
            'description': self.description,
            'date': self.date
        }

    @classmethod
    def from_dict(cls, data):
        """Create transaction from dictionary"""
        return cls(
            data['transaction_id'],
            data['student_id'],
            data['amount'],
            data.get('description', ''),
            data.get('date')
        )

    def __str__(self):
        return f"Transaction(ID: {self.transaction_id}, Student: {self.student_id}, Amount: Ksh.{self.amount:.2f})"

    def __lt__(self, other):
        """Less than comparison for BST (sort by amount)"""
        return self.amount < other.amount

    def __gt__(self, other):
        """Greater than comparison for BST"""
        return self.amount > other.amount
