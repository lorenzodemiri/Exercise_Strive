import sql_database

student = """CREATE TABLE IF NOT EXISTS student (
                name VARCHAR(20) PRIMARY KEY,
                surname VARCHAR(20) NOT NULL,
                id int NOT NULL,
                country VARCHAR(20),
                FOREIGN KEY(id) REFERENCES project(st) ON UPDATE CASCADE
        );"""


sql_database.sql_execute(student)

name = ['lorenzo', 'luca', 'paolo', 'giordano', 'mario', 'antonio', 'marco']
surname = ['rossi', 'pianta', 'zen', 'morelli', 'mansueti', 'scimmi', 'landi', 'cinelli']
country = ['it', 'uk', 'pl', 'es', 'it', 'fr', 'uk']
i = 1
for x,y,z in zip(name, surname, country):
    temp = """INSERT INTO student (name, surname, id, country) VALUES ('{}', '{}', {}, '{}')""".format(x,y,i,z)
    i += 1
    sql_database.sql_execute(temp)
    del temp

df = sql_database.pandas_select("select * from student")
print(df)
sql_database.close()
