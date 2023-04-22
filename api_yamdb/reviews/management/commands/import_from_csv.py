import csv

from django.db import IntegrityError

from reviews.models import User
from django.core.management.base import BaseCommand, CommandError
from reviews.models import Category, Genre, Title, TitleGenre


from api_yamdb.settings import BASE_DIR

CSV_FILES = {Category: 'category.csv',
             Genre: 'genre.csv',
             Title: 'titles.csv',
             TitleGenre: 'genre_title.csv',
             User: 'users.csv',
             }


class Command(BaseCommand):

    def handle(self, *args, **options):

        for model, csv_file in CSV_FILES.items():
            with open(f'{BASE_DIR}/static/data/{csv_file}',
                      'r', encoding='utf8') as file:
                for row in csv.DictReader(file, delimiter=','):
                    shallow_copy = row.copy()
                    for keys in shallow_copy.keys():
                        if 'category' in keys:
                            row['category_id'] = row.pop('category')
                        elif 'author' in keys:
                            row['author_id'] = row.pop('author')
                    try:
                        model.objects.create(**row)
                    except ValueError as e:
                        raise CommandError(
                            f'Ошибка: {e}, файл {file}, строка {row}'
                        )
                    except IntegrityError:
                        raise CommandError('База данных уже заполнена.'
                                           'Необходимо очистить БД')
            self.stdout.write(f'Таблица {model.__name__} импортирована!')