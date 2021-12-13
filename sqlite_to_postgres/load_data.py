import logging
import os
import sqlite3

import psycopg2
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor

from dc_movies import Film, Film_Genre, Film_Person, Genre, Person


def migrate_table(table: str, connection, pg_conn, sqcur, pgcur):
    sqcur.execute(f"""SELECT * FROM {table}""")
    with open('content.csv', 'w') as f:
        if table == 'film_work':
            while True:
                data = sqcur.fetchmany(100)
                if data:
                    for row in data:
                        temp = Film(
                            id=row['id'],
                            title=row['title'],
                            description=row['description'],
                            creation_date=row['creation_date'],
                            certificate=row['certificate'],
                            file_path=row['file_path'],
                            rating=row['rating'],
                            type=row['type'],
                            created_at=row['created_at'],
                            updated_at=row['updated_at']
                        )
                        f.write(f'''{temp.id}@{temp.title}@{temp.description}@\
{temp.creation_date}@{temp.certificate}@{temp.file_path}@\
{temp.rating}@{temp.type}@{temp.created_at}@{temp.updated_at}\n''')
                else:
                    break

        if table == 'genre':
            while True:
                data = sqcur.fetchmany(100)
                if data:
                    for row in data:
                        temp = Genre(
                            id=row['id'],
                            name=row['name'],
                            description=row['description'],
                            created_at=row['created_at'],
                            updated_at=row['updated_at']
                        )
                        f.write(f'''{temp.id}@{temp.name}@{temp.description}@\
{temp.created_at}@{temp.updated_at}\n''')
                else:
                    break

        if table == 'person':
            while True:
                data = sqcur.fetchmany(100)
                if data:
                    for row in data:
                        temp = Person(
                            id=row['id'],
                            full_name=row['full_name'],
                            birth_date=row['birth_date'],
                            updated_at=row['updated_at'],
                            created_at=row['created_at']
                        )
                        f.write(f'''{temp.id}@{temp.full_name}@\
{temp.birth_date}@{temp.updated_at}@{temp.created_at}\n''')
                else:
                    break

        if table == 'person_film_work':
            while True:
                data = sqcur.fetchmany(100)
                if data:
                    for row in data:
                        temp = Film_Person(
                            id=row['id'],
                            Film_Id=row['film_work_id'],
                            Person_Id=row['person_id'],
                            role=row['role'],
                            created_at=row['created_at'],
                        )
                        f.write(f'''{temp.id}@{temp.Film_Id}@\
{temp.Person_Id}@{temp.role}@{temp.created_at}\n''')
                else:
                    break

        if table == 'genre_film_work':
            while True:
                data = sqcur.fetchmany(100)
                if data:
                    for row in data:
                        temp = Film_Genre(
                            id=row['id'],
                            Film_Id=row['film_work_id'],
                            Genre_Id=row['genre_id'],
                            created_at=row['created_at']
                        )
                        f.write(f'''{temp.id}@{temp.Film_Id}@\
{temp.Genre_Id}@{temp.created_at}\n''')
                else:
                    break

    with open('content.csv', 'r') as f:
        try:
            pgcur.copy_from(f, table, sep='@', null='None')
            pg_conn.commit()
        except psycopg2.errors.UniqueViolation:
            logging.error(f'"{table}" date already exist')
            pgcur.execute("ROLLBACK")


def load_from_sqlite(
        connection: sqlite3.Connection,
        pg_conn: _connection
):
    connection.row_factory = sqlite3.Row
    sqcur = connection.cursor()
    pgcur = pg_conn.cursor()
    tables = (
        'film_work',
        'genre',
        'person',
        'genre_film_work',
        'person_film_work'
    )
    for tab in tables:
        migrate_table(tab, connection, pg_conn, sqcur, pgcur)

    os.system('rm content.csv')
    sqcur.close()
    pgcur.close()


if __name__ == '__main__':
    dsl = {
        'dbname': 'movies_database',
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT'),
        'options': '-c search_path=content'
    }
    with sqlite3.connect('db.sqlite') as sqlite_conn, psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
