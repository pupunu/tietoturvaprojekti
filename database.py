import sqlite3

def get_course(db, id):
    c = db.execute("SELECT course_name FROM courses where id = ?", [id]).fetchall()
    q = db.execute("SELECT id, question from questions where course_id = ?", [id]).fetchall()
    l = []

    for q in q:
        q_id = q[0]
        a = db.execute("SELECT answer, tf FROM Answers where question_id = ?", [q_id]).fetchall()
        l.append((q[1], a))


    return (c, l)

def add_course(db, name, teacher, q_list, )
    db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES ('selleri', 5)")
    db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES ('nauris', 8)")
    db.execute("INSERT INTO Tuotteet (nimi, hinta) VALUES ('lanttu', 4)")

if __name__ == "__main__":
    db = sqlite3.connect("database.db")
    db.isolation_level = None
    db.execute("CREATE TABLE Courses (id INTEGER PRIMARY KEY, name TEXT)")
    db.execute("CREATE TABLE Questions (id INTEGER PRIMARY KEY, question TEXT")
    db.execute("CREATE TABLE Aswers (id INTEGER PRIMARY KEY, answer TEXT, validity INTEGER")
    db.execute("CREATE TABLE Coursestudents (id INTEGER PRIMARY KEY, student TEXT, course_id INTEGER")
    print("database set")