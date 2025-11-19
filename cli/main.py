# cli/main.py
import sys
from library_manager.inventory import LibraryInventory
from library_manager.book import Book

# ---------------------------------------
# Utility UI functions
# ---------------------------------------

def line():
    print("-" * 60)

def header(title):
    line()
    print(f"{title.upper():^60}")
    line()

def prompt(text: str) -> str:
    return input(f"{text} ").strip()


# ---------------------------------------
# Flows
# ---------------------------------------

def add_book_flow(inv: LibraryInventory):
    header("Add a New Book")

    title = prompt("📘 Enter Title:")
    author = prompt("✍️  Enter Author:")
    isbn = prompt("🔖 Enter ISBN:")

    if not (title and author and isbn):
        print("\n⚠️  All fields are required. Try again.\n")
        return

    book = Book(title=title, author=author, isbn=isbn)
    inv.add_book(book)

    print("\n✅ Book successfully added!\n")


def issue_book_flow(inv: LibraryInventory):
    header("Issue a Book")

    isbn = prompt("📕 Enter ISBN to issue:")

    if not isbn:
        print("\n⚠️  ISBN is required.\n")
        return

    if inv.issue_book(isbn):
        print("\n📗 Book successfully issued!\n")
    else:
        print("\n❌ Unable to issue the book. Check logs.\n")


def return_book_flow(inv: LibraryInventory):
    header("Return a Book")

    isbn = prompt("📙 Enter ISBN to return:")

    if not isbn:
        print("\n⚠️  ISBN is required.\n")
        return

    if inv.return_book(isbn):
        print("\n📘 Book successfully returned!\n")
    else:
        print("\n❌ Unable to return the book. Check logs.\n")


def view_all_flow(inv: LibraryInventory):
    header("Library Catalog")

    books = inv.display_all()
    if not books:
        print("📭 No books found in the catalog.\n")
        return

    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book}")

    print()


def search_flow(inv: LibraryInventory):
    header("Search Books")

    print("Search by:")
    print("1. 🔎 Title")
    print("2. 🔍 ISBN\n")

    choice = prompt("Choose an option (1 or 2):")

    if choice == "1":
        title = prompt("Enter a keyword from the title:")
        results = inv.search_by_title(title)

        if results:
            print("\n📚 Results:")
            for b in results:
                print("•", b)
        else:
            print("\n❌ No books found with that title.")

    elif choice == "2":
        isbn = prompt("Enter ISBN:")
        book = inv.search_by_isbn(isbn)

        if book:
            print("\n📘 Book found:", book)
        else:
            print("\n❌ No book found with that ISBN.")
    else:
        print("\n⚠️ Invalid choice. Please select 1 or 2.")

    print()


# ---------------------------------------
# MAIN FUNCTION
# ---------------------------------------

def main():
    inv = LibraryInventory()

    print("\n" + "=" * 60)
    print(f"{'LIBRARY INVENTORY MANAGER':^60}")
    print("=" * 60)
    print(f"{'Created by: Tanishq':^60}")
    print(f"{'Roll No: 2501410009':^60}")  
    print(f"{'Branch: B.Tech CSE (Cyber Security)':^60}")
    print("=" * 60 + "\n")

    while True:
        header("Main Menu")

        print("1. ➕ Add Book")
        print("2. 📕 Issue Book")
        print("3. 📘 Return Book")
        print("4. 📚 View All Books")
        print("5. 🔍 Search Books")
        print("6. 🚪 Exit\n")

        choice = prompt("Choose an option (1–6):")

        if choice == "1":
            add_book_flow(inv)
        elif choice == "2":
            issue_book_flow(inv)
        elif choice == "3":
            return_book_flow(inv)
        elif choice == "4":
            view_all_flow(inv)
        elif choice == "5":
            search_flow(inv)
        elif choice == "6":
            print("\n👋 Goodbye!")
            sys.exit()
        else:
            print("\n⚠️ Invalid choice. Please enter a number between 1 and 6.\n")


# ---------------------------------------
# ENTRY POINT
# ---------------------------------------

if __name__ == "__main__":
    main()
