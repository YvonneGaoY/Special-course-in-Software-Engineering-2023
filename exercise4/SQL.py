import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('library.db')
c = conn.cursor()

# 执行 SQL 查询语句
book_id = input("Enter BookID: ")
c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Users.Name, Users.Email
              FROM Books
              LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
              LEFT JOIN Users ON Users.UserID = Reservations.UserID
              WHERE Books.BookID = ?''', (book_id,))

# 获取查询结果
results = c.fetchall()

# 打印查询结果
if results:
    for result in results:
        book_id, title, status, name, email = result
        print("Book ID:", book_id)
        print("Title:", title)
        print("Status:", status)
        if name:
            print("Reserved by:", name)
            print("Email:", email)
        print("-------------")
else:
    print("No matching books found.")
    

# 查询某个用户的预订情况
userid = input("Enter UserID: ")

c.execute('''SELECT Books.BookID, Books.Title, Books.Status, Reservations.ReservationDate
                  FROM Books
                  LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                  WHERE Reservations.UserID = ?''', (userid,))

results = c.fetchall()

if len(results) == 0:
    print("No reservations found.")
else:
    for row in results:
        book_id, title, status, reservation_date = row
        print(f"Book ID: {book_id}")
        print(f"Title: {title}")
        print(f"Status: {status}")
        print(f"Reservation Date: {reservation_date}\n")


# 查询某个预订的详细信息
reservation_id = input("Enter ReservationID: ")

c.execute('''SELECT Books.BookID, Books.Title, Books.Author, Books.ISBN, Books.Status, Users.Name, Users.Email, Reservations.ReservationDate
                  FROM Books
                  LEFT JOIN Reservations ON Books.BookID = Reservations.BookID
                  LEFT JOIN Users ON Users.UserID = Reservations.UserID
                  WHERE Reservations.ReservationID = ?''', (reservation_id,))

result = c.fetchone()

if result is None:
    print("Reservation not found.")
else:
    book_id, title, author, isbn, status, user_name, user_email, reservation_date = result
    print(f"Book ID: {book_id}")
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"ISBN: {isbn}")
    print(f"Status: {status}")

    if user_name is not None:
        print(f"Reserved by: {user_name} ({user_email})")
        print(f"Reservation Date: {reservation_date}")

# 关闭数据库连接
conn.close()