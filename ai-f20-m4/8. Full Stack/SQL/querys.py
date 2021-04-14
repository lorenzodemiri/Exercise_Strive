import sql_database as sql

#ex 1
std_count = "SELECT COUNT(name) FROM student"
print(sql.sql_query(std_count).fetchall())

#ex2
nlp = "SELECT student.name FROM student, project WHERE project.Topic = 'nlp' AND student.id = project.St"
print(sql.pandas_select(nlp))

#ex3
ml = "SELECT name FROM teacher WHERE speciality = 'ML' AND salary > 1200"
print(sql.pandas_select(ml))

#ex4

add_col = """ALTER TABLE student
                ADD COLUMN fav_teacher varchar(20)"""
sql.sql_execute(add_col)

#ex5

#ex6
un_std = "SELECT DISCTINCT(name) FROM student"
print(sql.sql_query(un_std).fetchall())

#ex7
join = "SELECT * FROM student INNER JOIN project ON student.id = project.St"
print(sql.pandas_select(join))

#ex8

max_grades = "SELECT student.name FROM student, project WHERE student.id = project.St AND max(project.Grade)"
print(sql.pandas_select(max_grades))
