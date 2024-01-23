from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

from django.db import models

NAME_LEN = 150
EMAIL_LEN = 254
ROLE_LEN = 20


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
    username = models.CharField(
        max_length=NAME_LEN,
        verbose_name='Имя пользователя',
        unique=True,
        db_index=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$',
            message='Имя пользователя содержит недопустимый символ'
        )]
    )
    email = models.EmailField(
        max_length=EMAIL_LEN,
        verbose_name='email',
    )
    first_name = models.CharField(
        max_length=NAME_LEN,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=NAME_LEN,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=ROLE_LEN,
        verbose_name='роль',
        choices=CHOICES,
        default=USER
    )

    class Meta:
        ordering = ["id", ]

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
