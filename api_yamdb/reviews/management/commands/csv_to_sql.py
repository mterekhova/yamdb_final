import csv
import sqlite3
from abc import ABC

from django.conf import settings
from django.core.management import BaseCommand
from users.models import User

from ...models import Category, Genre, Title, TitleGenres


class Command(BaseCommand, ABC):
    help = 'Converting CSV to SQL'

    def handle(self, *args, **options):
        dir_name = f'{settings.BASE_DIR}/static/data'
        db = sqlite3.connect('db.sqlite3')
        db_cursor = db.cursor()

        with open(f'{dir_name}/users.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                User.objects.create(
                    username=row[1],
                    email=row[2],
                    role=row[3]
                )
        with open(f'{dir_name}/category.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                Category.objects.create(
                    name=row[1],
                    slug=row[2]
                )
        with open(f'{dir_name}/titles.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                Title.objects.create(
                    name=row[1],
                    year=int(row[2]),
                    category=Category(id=int(row[3]))
                )
        with open(f'{dir_name}/review.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                db_cursor.execute(
                    "INSERT INTO reviews_review(title_id, text, author_id,"
                    " score, pub_date) VALUES (?,?,?,?,?)",
                    (
                        int(row[1]),
                        str(row[2]),
                        int(row[3]),
                        int(row[4]),
                        str(row[5])
                    )
                )
                db.commit()
        with open(f'{dir_name}/comments.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                db_cursor.execute(
                    "INSERT INTO reviews_comment(text, pub_date, author_id,"
                    " review_id) VALUES (?,?,?,?)",
                    (
                        str(row[2]),
                        str(row[4]),
                        int(row[3]),
                        int(row[1]),
                    )
                )
                db.commit()
        with open(f'{dir_name}/genre.csv', 'r', encoding='UTF-8') as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                Genre.objects.create(
                    name=row[1],
                    slug=row[2]
                )
        with open(f'{dir_name}/genre_title.csv', 'r', encoding='UTF-8')\
                as file:
            csv_reader = csv.reader(file)
            list_csv = list(csv_reader)
            for row in list_csv[1:]:
                TitleGenres.objects.create(
                    title=Title(id=int(row[1])),
                    genre=Genre(id=int(row[2]))
                )
