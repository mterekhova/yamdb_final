from django.contrib.auth.models import AbstractUser
from django.db import models

ROLES_CHOICES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Администратор'),
]


class User(AbstractUser):
    email = models.EmailField('email address', blank=True, unique=True)
    bio = models.TextField(
        'Биография',
        blank=True,)
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLES_CHOICES,
        default='user',
    )


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title
