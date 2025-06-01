import os
import json

BOOKS_FILE = 'books.txt'
STUDENTS_FILE = 'students.txt'
LOANS_FILE = 'loans.txt'

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return []

def save_data(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

def add_book():
    books = load_data(BOOKS_FILE)
    title = input("Tytuł: ")
    author = input("Autor: ")
    year = input("Rok wydania: ")
    pages = input("Ilość stron: ")
    copies = int(input("Ilość egzemplarzy: "))

    books.append({
        "title": title,
        "author": author,
        "year": year,
        "pages": pages,
        "copies": copies
    })
    save_data(BOOKS_FILE, books)
    print("📚 Książka dodana!")

def list_books():
    books = load_data(BOOKS_FILE)
    if not books:
        print("📭 Brak książek w katalogu.")
        return
    for idx, book in enumerate(books, 1):
        print(f"{idx}. {book['title']} - {book['author']} ({book['year']}), stron: {book['pages']}, egz.: {book['copies']}")

def edit_book():
    books = load_data(BOOKS_FILE)
    list_books()
    idx = int(input("Podaj numer książki do edycji: ")) - 1
    if 0 <= idx < len(books):
        book = books[idx]
        book['title'] = input(f"Nowy tytuł ({book['title']}): ") or book['title']
        book['author'] = input(f"Nowy autor ({book['author']}): ") or book['author']
        book['year'] = input(f"Nowy rok wydania ({book['year']}): ") or book['year']
        book['pages'] = input(f"Nowa ilość stron ({book['pages']}): ") or book['pages']
        book['copies'] = int(input(f"Nowa ilość egzemplarzy ({book['copies']}): ") or book['copies'])
        save_data(BOOKS_FILE, books)
        print("✏️ Książka zaktualizowana!")
    else:
        print("❌ Nieprawidłowy numer książki.")

def delete_book():
    books = load_data(BOOKS_FILE)
    list_books()
    idx = int(input("Podaj numer książki do usunięcia: ")) - 1
    if 0 <= idx < len(books):
        books.pop(idx)
        save_data(BOOKS_FILE, books)
        print("🗑️ Książka usunięta.")
    else:
        print("❌ Nieprawidłowy numer książki.")

def add_student():
    students = load_data(STUDENTS_FILE)
    name = input("Imię i nazwisko studenta: ")
    if name not in students:
        students.append(name)
        save_data(STUDENTS_FILE, students)
        print("👤 Student dodany.")
    else:
        print("⚠️ Student już istnieje.")

def loan_book():
    books = load_data(BOOKS_FILE)
    students = load_data(STUDENTS_FILE)
    loans = load_data(LOANS_FILE)

    student = input("Imię i nazwisko studenta: ")
    if student not in students:
        print("❌ Student nie istnieje.")
        return

    student_loans = [l for l in loans if l['student'] == student]
    if len(student_loans) >= 5:
        print("⚠️ Student ma już 5 książek wypożyczonych.")
        return

    list_books()
    idx = int(input("Podaj numer książki do wypożyczenia: ")) - 1
    if 0 <= idx < len(books):
        if books[idx]['copies'] > 0:
            books[idx]['copies'] -= 1
            loans.append({"student": student, "title": books[idx]['title']})
            save_data(BOOKS_FILE, books)
            save_data(LOANS_FILE, loans)
            print("✅ Książka wypożyczona.")
        else:
            print("❌ Brak dostępnych egzemplarzy.")
    else:
        print("❌ Nieprawidłowy numer książki.")

def return_book():
    loans = load_data(LOANS_FILE)
    books = load_data(BOOKS_FILE)
    student = input("Imię i nazwisko studenta: ")

    student_loans = [l for l in loans if l['student'] == student]
    if not student_loans:
        print("❌ Brak wypożyczeń.")
        return

    for idx, loan in enumerate(student_loans, 1):
        print(f"{idx}. {loan['title']}")
    choice = int(input("Wybierz książkę do zwrotu: ")) - 1

    if 0 <= choice < len(student_loans):
        book_title = student_loans[choice]['title']
        for book in books:
            if book['title'] == book_title:
                book['copies'] += 1
                break
        loans.remove(student_loans[choice])
        save_data(BOOKS_FILE, books)
        save_data(LOANS_FILE, loans)
        print("📥 Książka zwrócona.")
    else:
        print("❌ Nieprawidłowy wybór.")

def report_loans():
    loans = load_data(LOANS_FILE)
    if not loans:
        print("📭 Brak wypożyczeń.")
        return
    print("\n📄 Aktualne wypożyczenia:")
    for loan in loans:
        print(f"{loan['student']} ➜ {loan['title']}")

def menu():
    while True:
        print("\n--- BIBLIOTEKA ---")
        print("1. Dodaj książkę")
        print("2. Edytuj książkę")
        print("3. Usuń książkę")
        print("4. Pokaż wszystkie książki")
        print("5. Dodaj studenta")
        print("6. Wypożycz książkę")
        print("7. Zwróć książkę")
        print("8. Raport wypożyczeń")
        print("9. Wyjście")

        choice = input("Wybierz opcję: ")

        match choice:
            case "1": add_book()
            case "2": edit_book()
            case "3": delete_book()
            case "4": list_books()
            case "5": add_student()
            case "6": loan_book()
            case "7": return_book()
            case "8": report_loans()
            case "9": print("👋 Do widzenia!"); break
            case _: print("❌ Nieprawidłowy wybór.")

if __name__ == "__main__":
    menu()
