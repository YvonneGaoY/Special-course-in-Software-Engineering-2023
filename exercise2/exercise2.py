# # f = open("stephen_king_adaptations.txt")
# import sqlite3
# with open('stephen_king_adaptations.txt') as f:
#     stephen_king_adaptations_list = list(map(lambda line: line.rstrip(), f))
# print('list:', stephen_king_adaptations_list)


# try:
#     newConnection = sqlite3.connect('stephen_king_adaptations.db')
#     cursor = newConnection.cursor()

#     newQuery = ''')'''

#     cursor.execute(
#         "create table if not exists stephen_king_adaptations_table(movieID, movieName, movieYear, imdbRating)")

#     for adaptation in stephen_king_adaptations_list:
#         movieID, movieName, movieYear, imdbRating = adaptation.split(',')
#         # type(int(movieYear))
#         # type(float(imdbRating))
#         cursor.execute("INSERT INTO stephen_king_adaptations_table(movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)",
#                        (movieID, movieName, movieYear, imdbRating))
#     while True:
#         username = input(
#             "Please enter the serial number of your choice：1. Movie name\n 2. Movie year\n3. Movie rating\n4. STOP")
#         if username == 1:
#             name = input("Please enter the move name:")
#             cursor.execute(
#                 "SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (name))
#             results = cursor.fetchall()
#             if len(results) > 0:
#                 for row in results:
#                     movieID, movieName, movieYear, imdbRating = row
#                     print(f"Movie ID: {movieID}")
#                     print(f"Movie Name: {movieName}")
#                     print(f"Movie Year: {movieYear}")
#                     print(f"IMDb Rating: {imdbRating}")
#                     print("--------------------")
#             else:
#                 print("No such movie exists in our database")
#                 cursor.close()
#         elif username == 2:
#             year = input("Please enter the move year:")
#             cursor.execute(
#                 "SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (year))
#             results = cursor.fetchall()
#             if len(results) > 0:
#                 for row in results:
#                     movieID, movieName, movieYear, imdbRating = row
#                     print(f"Movie ID: {movieID}")
#                     print(f"Movie Name: {movieName}")
#                     print(f"Movie Year: {movieYear}")
#                     print(f"IMDb Rating: {imdbRating}")
#                     print("--------------------")
#             else:
#                 print("No movies were found for that year in our database.")
#                 cursor.close()
#         elif username == 3:
#             rating = input("Please enter the movie rating:")
#             cursor.execute(
#                 "SELECT * FROM stephen_king_adaptations_table WHERE imdbRating=?", (rating))
#             results = cursor.fetchall()
#             if len(results) > 0:
#                 for row in results:
#                     movieID, movieName, movieYear, imdbRating = row
#                     print(f"Movie ID: {movieID}")
#                     print(f"Movie Name: {movieName}")
#                     print(f"Movie Year: {movieYear}")
#                     print(f"IMDb Rating: {imdbRating}")
#                     print("--------------------")
#             else:
#                 print("No movies at or above that rating were found in the database")
#                 cursor.close()
#         elif username == 4:
#             "STOP" == input("Please enter the movie rating:")
#             break

#     # cursor.execute("insert into stephen_kind_adaptations_table values() ",stephen_king_adaptations_list)

#     newConnection.commit()

#     cursor.close()
# except sqlite3.Error as error:
#     print("Something didn't go well ", error)
# finally:
#     if newConnection():
#         newConnection.close()
import sqlite3

with open('stephen_king_adaptations.txt') as f:
    stephen_king_adaptations_list = list(map(lambda line: line.rstrip(), f))
print('list:', stephen_king_adaptations_list)

try:
    newConnection = sqlite3.connect('stephen_king_adaptations.db')
    cursor = newConnection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table(movieID TEXT, movieName TEXT, movieYear INTEGER, imdbRating REAL)")

    for adaptation in stephen_king_adaptations_list:
        movieID, movieName, movieYear, imdbRating = adaptation.split(',')
        cursor.execute("INSERT INTO stephen_king_adaptations_table(movieID, movieName, movieYear, imdbRating) VALUES (?, ?, ?, ?)",
                       (movieID, movieName, int(movieYear), float(imdbRating)))

    while True:
        username = input(
            "Please enter the serial number of your choice: 1. Movie name\n 2. Movie year\n 3. Movie rating\n 4. STOP")
        if int(username) == 1:
            name = input("Please enter the movie name:")
            cursor.execute(
                "SELECT * FROM stephen_king_adaptations_table WHERE movieName=?", (name,))
            results = cursor.fetchall()
            if len(results) > 0:
                for row in results:
                    movieID, movieName, movieYear, imdbRating = row
                    print(f"Movie ID: {movieID}")
                    print(f"Movie Name: {movieName}")
                    print(f"Movie Year: {movieYear}")
                    print(f"IMDb Rating: {imdbRating}")
                    print("--------------------")
            else:
                print("No such movie exists in our database")
        elif int(username) == 2:
            year = input("Please enter the movie year:")
            cursor.execute(
                "SELECT * FROM stephen_king_adaptations_table WHERE movieYear=?", (int(year),))
            results = cursor.fetchall()
            if len(results) > 0:
                for row in results:
                    movieID, movieName, movieYear, imdbRating = row
                    print(f"Movie ID: {movieID}")
                    print(f"Movie Name: {movieName}")
                    print(f"Movie Year: {movieYear}")
                    print(f"IMDb Rating: {imdbRating}")
                    print("--------------------")
            else:
                print("No movies were found for that year in our database.")
        elif int(username) == 3:
            rating = input("Please enter the movie rating:")
            cursor.execute(
                "SELECT * FROM stephen_king_adaptations_table WHERE imdbRating>=?", (float(rating),))
            results = cursor.fetchall()
            if len(results) > 0:
                for row in results:
                    movieID, movieName, movieYear, imdbRating = row
                    print(f"Movie ID: {movieID}")
                    print(f"Movie Name: {movieName}")
                    print(f"Movie Year: {movieYear}")
                    print(f"IMDb Rating: {imdbRating}")
                    print("--------------------")
            else:
                print("No movies at or above that rating were found in the database")
        elif int(username) == 4:
            break

    newConnection.commit()

except sqlite3.Error as error:
    print("Something didn't go well: ", error)

finally:
    if newConnection:
        newConnection.close()


