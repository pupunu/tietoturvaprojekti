CREATE TABLE Courses (id INTEGER PRIMARY KEY, course_name TEXT, teacher TEXT);
CREATE TABLE Questions (id INTEGER PRIMARY KEY, question TEXT, course_id INTEGER);
CREATE TABLE Answers (id INTEGER PRIMARY KEY, question_id INTEGER, answer TEXT, TF INTEGER);
CREATE TABLE Course_registration (id INTEGER PRIMARY KEY, student TEXT, course_id INTEGER);

INSERT INTO Courses (course_name) values ("testi");
INSERT INTO Questions (question) VALUES ('Mitä kello on?', (select id from courses where course_name = "testi"));
INSERT INTO Answers (answer, question_id, TF) values ("Squirtle", (select id from questions where question_name = "Mitä kello on?", 1));
INSERT INTO Answers (answer, question_id, TF) values ("Bulbasaur", (select id from questions where question_name = "Mitä kello on?", 0));
INSERT INTO Answers (answer, question_id, TF) values ("Charmander", (select id from questions where question_name = "Mitä kello on?", 0));