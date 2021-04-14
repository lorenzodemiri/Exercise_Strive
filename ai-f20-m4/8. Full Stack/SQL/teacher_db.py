import sql_database

teacher = """CREATE TABLE IF NOT EXISTS teacher (
                name VARCHAR(20),
                surname VARCHAR(20) NOT NULL,
                id int NOT NULL PRIMARY KEY,
                country VARCHAR(20),
                speciality VARCHAR(20) NOT NULL,
                salary int,
                FOREIGN KEY(id) REFERENCES project(st)
        );"""


sql_database.sql_execute(teacher)

name = ['jan', 'Javier', 'Antonion', 'Jon', 'George']
surname = ['Carbonell', 'Perez', 'Marsella', 'Perez', 'Studentko']
country = ['es','es','it','es','pl']
spec = ['Head', 'ML', 'Python','DB', 'CV']
salaries = ['1500', '1300', '1200', '1200', '750']

i = 1
for x, y, z, v, t in zip(name, surname, country, spec, salaries):
    temp = """INSERT INTO student (name, surname, id, country, speciality, salary) VALUES ('{}', '{}', {}, '{}', '{}', '{}')""".format(
        x, y, i, z, v, t)
    i += 1
    sql_database.sql_execute(temp)
    del temp

df = sql_database.pd_select("select * from teacher")
print(df)
sql_database.close()
