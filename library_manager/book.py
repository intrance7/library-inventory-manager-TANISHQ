# library_manager/book.py
from dataclasses import dataclass, asdict


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    status: str = "available"  # "available" or "issued"

    def __post_init__(self):
        # Normalize status
        self.status = self.status.lower()

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {self.status}"

    def to_dict(self) -> dict:
        """Return a dict representation suitable for JSON persistence."""
        return asdict(self)

    def is_available(self) -> bool:
        return self.status == "available"

    def issue(self) -> bool:
        """Attempt to issue the book. Return True if successful."""
        if self.is_available():
            self.status = "issued"
            return True
        return False

    def return_book(self) -> bool:
        """Attempt to return the book. Return True if successful."""
        if not self.is_available():
            self.status = "available"
            return True
        return False
