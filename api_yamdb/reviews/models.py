from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

NAME_LEN = 256
SLUG_LEN = 50


class Category(models.Model):
    name = models.CharField(max_length=NAME_LEN)
    slug = models.SlugField(max_length=SLUG_LEN, unique=True)

    def __str__(self):
        return self.name


class Genres(models.Model):
    name = models.CharField(max_length=NAME_LEN)
    slug = models.SlugField(max_length=SLUG_LEN, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=NAME_LEN)
    year = models.IntegerField()
    description = models.TextField()
    genre = models.ManyToManyField(Genres, related_name="genres")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL,
                                 null=True)
    rating = models.FloatField(null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Комментарий',
        null=True)
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.SmallIntegerField(validators=[MaxValueValidator(10),
                                                 MinValueValidator(0)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=['title', 'author'],
                                               name='unique_review'), ]


class Comments(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
