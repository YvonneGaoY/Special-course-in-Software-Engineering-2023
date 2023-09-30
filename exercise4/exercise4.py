import sqlite3

def connect_to_database(database_file):
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()
    return cursor, conn

def create_books_table(cursor, conn):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Books (
                        BookID INTEGER PRIMARY KEY,
                        Title TEXT,
                        Author TEXT,
                        ISBN TEXT,
                        Status TEXT
                    )''')
    conn.commit()

def create_users_table(cursor, conn):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        UserID INTEGER PRIMARY KEY,
                        Name TEXT,
                        Email TEXT
                    )''')
    conn.commit()

def create_reservations_table(cursor, conn):
    cursor.execute('''CREATE TABLE IF NOT EXISTS Reservations (
                        ReservationID INTEGER PRIMARY KEY,
                        BookID INTEGER,
                        UserID INTEGER,
                        ReservationDate TEXT,
                        FOREIGN KEY (BookID) REFERENCES Books (BookID),
                        FOREIGN KEY (UserID) REFERENCES Users (UserID)
                    )''')
    conn.commit()

def add_book(cursor, conn, title, author, isbn, status):
    cursor.execute('''INSERT INTO Books (Title, Author, ISBN, Status)
                      VALUES (?,?,?,?)''', (title, author, isbn, status))
    conn.commit()
    print(f"{cursor.rowcount} record(s) inserted.")

def find_book_detail(cursor, book_id):
    query = '''
        SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Users.UserID = Reservations.UserID
        WHERE Books.BookID = ?
    '''
    cursor.execute(query, (book_id,))
    result = cursor.fetchone()

    if result is None:
        print("Book not found.")
    else:
        book_id, title, status, user_name, user_email = result
        print(f"Book ID: {book_id}")
        print(f"Title: {title}")
        print(f"Status: {status}")

        if user_name is None:
            print("This book is not reserved.")
        else:
            print(f"This book is reserved by {user_name} ({user_email}).")


def find_reservation_status(cursor, search_text):
    if search_text.startswith('LB'):
        column = 'Books.BookID'
        value = search_text[2:]
    elif search_text.startswith('LU'):
        column = 'Users.UserID'
        value = search_text[2:]
    elif search_text.startswith('LR'):
        column = 'Reservations.ReservationID'
        value = search_text[2:]
    else:
        column = 'Books.Title'
        value = search_text

    query = f'''
        SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email, Reservations.ReservationID
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Users.UserID = Reservations.UserID
        WHERE {column} = ?
    '''
    cursor.execute(query, (value,))
    result = cursor.fetchone()

    if result is None:
        print("Book or reservation not found.")
    else:
        book_id, title, status, user_name, user_email, reservation_id = result
        print(f"Book ID: {book_id}")
        print(f"Title: {title}")
        print(f"Status: {status}")

        if reservation_id is not None:
            print(f"Reservation ID: {reservation_id}")

        if user_name is not None:
            print(f"Reserved by: {user_name} ({user_email})")

def find_all_books(cursor):
    query = '''
        SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
        FROM Books
        LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
        LEFT JOIN Users ON Users.UserID = Reservations.UserID
    '''
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        print("No books found.")
    else:
        for row in results:
            book_id, title, author, isbn, status, user_name,user_email,reservation_date = row
            print(f"Book ID: {book_id}")
            print(f"Title: {title}")
            print(f"Author: {author}")
            print(f"ISBN: {isbn}")
            print(f"Status: {status}")

            if user_name is not None:
                print(f"Reserved by: {user_name} ({user_email})")
                print(f"Reservation Date: {reservation_date}")
            
            print()



import datetime

def update_book_details(cursor, conn, book_id, title=None, author=None, isbn=None, status=None):
    if status is not None:
        cursor.execute('''UPDATE Books SET Status = ? WHERE BookID = ?''', (status, book_id))
        conn.commit()
        print(f"Book ID {book_id} status updated to {status}.")
        
        if status == "Reserved":
            reservation_id = generate_reservation_id(cursor)
            user_id = input("Enter UserID: ")
            name = input("Enter Name: ")
            email = input("Enter Email: ")
            reservation_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            cursor.execute('''INSERT INTO Reservations (ReservationID, BookID, UserID, ReservationDate) VALUES (?, ?, ?, ?)''', (reservation_id, book_id, user_id, reservation_date))
            conn.commit()
            print(f"A new reservation has been added for Book ID {book_id}.")
            
            cursor.execute('''INSERT INTO Users (UserID, Name, Email) VALUES (?, ?, ?)''', (user_id, name, email))
            conn.commit()
            print(f"A new user has been added with UserID {user_id}.")
            
    else:
        if title is not None:
            cursor.execute('''UPDATE Books SET Title = ? WHERE BookID = ?''', (title, book_id))
            conn.commit()
        
        if author is not None:
            cursor.execute('''UPDATE Books SET Author = ? WHERE BookID = ?''', (author, book_id))
            conn.commit()
        
        if isbn is not None:
            cursor.execute('''UPDATE Books SET ISBN = ? WHERE BookID = ?''', (isbn, book_id))
            conn.commit()

        print(f"Book ID {book_id} details updated.")

def generate_reservation_id(cursor):
    cursor.execute('''SELECT MAX(ReservationID) FROM Reservations''')
    result = cursor.fetchone()[0]
    if result is not None:
        return result + 1
    else:
        return 1


def delete_book(cursor, conn, book_id):
    cursor.execute('''DELETE FROM Books WHERE BookID = ?''', (book_id,))
    cursor.execute('''DELETE FROM Reservations WHERE BookID = ?''', (book_id,))
    conn.commit()
    print(f"{cursor.rowcount} record(s) deleted.")

def main():
    cursor, conn = connect_to_database('library.db')
    create_books_table(cursor, conn)
    create_users_table(cursor, conn)
    create_reservations_table(cursor, conn)

    while True:
        print("1. Add a new book")
        print("2. Find a book's detail based on BookID")
        print("3. Find a book's reservation status based on BookID(LB), Title, UserID(LU), and ReservationID(LR)")
        print("4. Find all books in the database")
        print("5. Modify/update book details based on BookID")
        print("6. Delete a book based on BookID")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            title = input("Enter book title: ")
            author = input("Enter book author: ")
            isbn = input("Enter book ISBN: ")
            status = input("Enter book status: ")
            add_book(cursor, conn, title, author, isbn, status)

        elif choice == "2":
            book_id = int(input("Enter BookID: "))
            find_book_detail(cursor, book_id)

        elif choice == "3":
            search_text = input("Enter BookID, Title, UserID, or ReservationID: ")
            find_reservation_status(cursor, search_text)

        elif choice == "4":
            find_all_books(cursor)

        elif choice == "5":
            book_id = int(input("Enter BookID: "))
            title = input("Enter updated title (leave blank to skip): ")
            author = input("Enter updated author (leave blank to skip): ")
            isbn = input("Enter updated ISBN (leave blank to skip): ")
            status = input("Enter updated status (leave blank to skip): ")
            update_book_details(cursor, conn, book_id, title, author, isbn, status)

        elif choice == "6":
            book_id = int(input("Enter BookID: "))
            delete_book(cursor, conn, book_id)

        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")
            
            
    

    conn.close()

if __name__ == "__main__":
    main()
