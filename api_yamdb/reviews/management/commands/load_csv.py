import csv
import pathlib

from django.core.management.base import BaseCommand
from django.shortcuts import get_object_or_404

from reviews.models import Category, Genres, Title, User, Comments, Review


class Command(BaseCommand):
    help = 'load csv files to sql database'

    def handle(self, *args, **options):
        category_path = pathlib.Path("static/data/category.csv")
        with open(category_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                category = Category(id=id, name=name, slug=slug)
                category.save()

        genre_path = pathlib.Path("static/data/genre.csv")
        with open(genre_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                slug = row['slug']
                genres = Genres(id=id, name=name, slug=slug)
                genres.save()

        titles_path = pathlib.Path("static/data/titles.csv")
        with open(titles_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                name = row['name']
                year = row['year']
                category_id = row['category']
                titles = Title(id=id, name=name, year=year,
                               category_id=category_id)
                titles.save()

        genre_title_path = pathlib.Path("static/data/genre_title.csv")
        with open(genre_title_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                genre_id = row['genre_id']
                titles = get_object_or_404(Title, id=title_id)
                genres = get_object_or_404(Genres, id=genre_id)
                titles.genre.add(genres)
                titles.save()

        users_path = pathlib.Path("static/data/users.csv")
        with open(users_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                username = row['username']
                email = row['email']
                role = row['role']
                bio = row['bio']
                first_name = row['first_name']
                last_name = row['last_name']
                users = User(id=id, username=username, email=email,
                             role=role, bio=bio, first_name=first_name,
                             last_name=last_name)
                users.save()

        review_path = pathlib.Path("static/data/review.csv")
        with open(review_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                title_id = row['title_id']
                text = row['text']
                author = row['author']
                score = row['score']
                pub_date = row['pub_date']
                reviews = Review(id=id, title_id=title_id,
                                 text=text, author=User.objects.get(id=author),
                                 score=score,
                                 pub_date=pub_date)
                reviews.save()

        comments_path = pathlib.Path("static/data/comments.csv")
        with open(comments_path.absolute(),
                  encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file, delimiter=',')
            for row in csv_reader:
                id = row['id']
                review_id = row['review_id']
                text = row['text']
                author = row['author']
                pub_date = row['pub_date']
                comments = Comments(id=id, review_id=review_id, text=text,
                                    pub_date=pub_date,
                                    author=User.objects.get(id=author))
                comments.save()
