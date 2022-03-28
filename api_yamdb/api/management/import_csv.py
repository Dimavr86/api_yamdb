import csv
import os

from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User


class Command(BaseCommand):
    DATA_DIR = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../../static/data/'))

    def create_genre_title(self, row):
        title = Title.objects.get(
            pk=row['title_id'],
        )
        title.genre.add(Genre.objects.get(pk=row['genre_id']))
        title.save()

    def create_review(self, row):
        Review.objects.create(
            pk=row['id'],
            author=User.objects.get(pk=row['author']),
            title=Title.objects.get(pk=row['title_id']),
            text=row['text'],
            score=row['score'],
            pub_date=row['pub_date'],
        )

    def create_comments(self, row):
        Comment.objects.create(
            pk=row['id'],
            author=User.objects.get(pk=row['author']),
            review=Review.objects.get(pk=row['review_id']),
            text=row['text'],
            pub_date=row['pub_date'],
        )

    def create_users(self, row):
        User.objects.create(
            pk=row['id'],
            username=row['username'],
            email=row['email'],
            role=row['role'],
            bio=row['bio'],
            first_name=row['first_name'],
            last_name=row['last_name'],
        )

    def create_category(self, row):
        Category.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def create_genre(self, row):
        Genre.objects.create(
            pk=row['id'],
            name=row['name'],
            slug=row['slug'],
        )

    def create_titles(self, row):
        Title.objects.create(
            pk=row['id'],
            category=Category.objects.get(pk=row['category']),
            name=row['name'],
            year=row['year'],
        )

    CSV_NAMES = [
        ('users', create_users),
        ('category', create_category),
        ('genre', create_genre),
        ('titles', create_titles),
        ('genre_title', create_genre_title),
        ('review', create_review),
        ('comments', create_comments),
    ]

    def import_data(self, file):
        try:
            with open(Command.DATA_DIR + f'\\{file[0]}.csv',
                      encoding='utf-8', newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    file[1](self, row)
        except Exception as err:
            self.stdout.write(self.style.ERROR(
                f'Ошибка импорта {file[0]}: {err}'
            ))
        else:
            self.stdout.write(self.style.SUCCESS(
                f'{file[0]}: данные загружены успешно'
            ))

    def handle(self, *args, **kwargs):
        for file in self.CSV_NAMES:
            self.import_data(file)
