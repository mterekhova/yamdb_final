from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Title(models.Model):
    name = models.CharField(max_length=256,
                            verbose_name='Название произведения')
    year = models.IntegerField(verbose_name='Год выхода')
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
        blank=True,
        verbose_name='Категория')
    genre = models.ManyToManyField(
        'Genre',
        through='TitleGenres',
        related_name='titles',
        blank=True,
        verbose_name='Жанр'
    )
    description = models.TextField(null=True,
                                   blank=True,
                                   verbose_name='Описание')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True,
                            verbose_name='Адрес для страницы с категорией')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100,
                            verbose_name='Название жанра')
    slug = models.SlugField(verbose_name='URL страницы с выбранным жанром',
                            unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class TitleGenres(models.Model):
    title = models.ForeignKey('Title',
                              on_delete=models.CASCADE,
                              verbose_name='Произведение')
    genre = models.ForeignKey('Genre',
                              on_delete=models.CASCADE,
                              verbose_name='Жанр')

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'{self.title} {self.genre}'


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        verbose_name = 'Отзыв на произведение'
        verbose_name_plural = 'Отзывы на произведение'
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='author_title_constraint'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий к отзыву'
        verbose_name_plural = 'Комментарии к отзыву'

    def __str__(self):
        return self.text
