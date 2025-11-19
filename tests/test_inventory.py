# tests/test_inventory.py
import os
import tempfile
from library_manager.inventory import LibraryInventory
from library_manager.book import Book


def test_add_issue_return_and_persistence(tmp_path):
    storage_file = tmp_path / "test_books.json"
    inv = LibraryInventory(storage_path=str(storage_file))

    b = Book(title="Test Driven", author="Author A", isbn="ISBN-1234")
    inv.add_book(b)
    assert inv.search_by_isbn("ISBN-1234") is not None

    assert inv.issue_book("ISBN-1234") is True
    assert inv.search_by_isbn("ISBN-1234").status == "issued"

    assert inv.return_book("ISBN-1234") is True
    assert inv.search_by_isbn("ISBN-1234").status == "available"

    # Ensure persistence
    inv.save()
    new_inv = LibraryInventory(storage_path=str(storage_file))
    assert new_inv.search_by_isbn("ISBN-1234") is not None
