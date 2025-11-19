# library_manager/inventory.py
import json
import logging
from pathlib import Path
from typing import List, Optional

from .book import Book

logger = logging.getLogger(__name__)


class LibraryInventory:
    def __init__(self, storage_path: str = "books.json"):
        self.storage = Path(storage_path)
        self.books: List[Book] = []
        self._setup_logging()
        self.load()

    def _setup_logging(self):
        handler = logging.StreamHandler()
        fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(fmt)
        root = logging.getLogger()
        if not root.handlers:
            root.addHandler(handler)
        root.setLevel(logging.INFO)

    def add_book(self, book: Book) -> None:
        if self.search_by_isbn(book.isbn):
            logger.error("Book with ISBN %s already exists. Skipping add.", book.isbn)
            return
        self.books.append(book)
        logger.info("Added book: %s", book)
        self.save()

    def search_by_title(self, title: str) -> List[Book]:
        title_lower = title.strip().lower()
        return [b for b in self.books if title_lower in b.title.lower()]

    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        isbn = isbn.strip()
        for b in self.books:
            if b.isbn == isbn:
                return b
        return None

    def display_all(self) -> List[str]:
        return [str(b) for b in self.books]

    def issue_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.error("No book found with ISBN %s", isbn)
            return False
        if book.issue():
            logger.info("Issued book: %s", book)
            self.save()
            return True
        logger.error("Book %s is already issued.", isbn)
        return False

    def return_book(self, isbn: str) -> bool:
        book = self.search_by_isbn(isbn)
        if not book:
            logger.error("No book found with ISBN %s", isbn)
            return False
        if book.return_book():
            logger.info("Returned book: %s", book)
            self.save()
            return True
        logger.error("Book %s was not issued.", isbn)
        return False

    def save(self) -> None:
        """Save books list to JSON. Use try/except to handle IO errors."""
        try:
            data = [b.to_dict() for b in self.books]
            with self.storage.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            logger.info("Saved %d books to %s", len(self.books), self.storage)
        except Exception as e:
            logger.exception("Failed to save books: %s", e)

    def load(self) -> None:
        """Load books from JSON. If file missing or corrupted, start with empty list."""
        if not self.storage.exists():
            logger.info("%s not found. Starting with empty catalog.", self.storage)
            self.books = []
            return
        try:
            with self.storage.open("r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = []
            for item in data:
                # Validate and fill missing fields defensively
                title = item.get("title", "Unknown Title")
                author = item.get("author", "Unknown Author")
                isbn = item.get("isbn", "")
                status = item.get("status", "available")
                loaded.append(Book(title=title, author=author, isbn=isbn, status=status))
            self.books = loaded
            logger.info("Loaded %d books from %s", len(self.books), self.storage)
        except json.JSONDecodeError:
            logger.error("JSON decode error reading %s. Backing up corrupted file and starting fresh.", self.storage)
            # Optionally back up corrupted file
            try:
                backup = self.storage.with_suffix(".corrupt.json")
                self.storage.replace(backup)
                logger.info("Moved corrupted file to %s", backup)
            except Exception:
                logger.exception("Failed to back up corrupted file.")
            self.books = []
        except Exception as e:
            logger.exception("Unexpected error while loading books: %s", e)
            self.books = []
