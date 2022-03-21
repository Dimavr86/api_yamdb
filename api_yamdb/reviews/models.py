from django.db import models
import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    name = models.TextField(
        'Название категории',
        max_length=255
    )
    slug = models.SlugField(
        unique=True,
        max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = (
            'slug',
        )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.TextField(max_length=255
    )
    slug = models.SlugField(
        unique=True,
        max_length=100
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = (
            'slug',
        )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.TextField(
        'Название произведения',
        max_length=255
    )
    description = models.TextField('Описание', blank=True)
    year = models.PositiveSmallIntegerField(
        'Год издания',
        blank=False,
        null=False,
        validators=[
            MaxValueValidator(
                dt.datetime.now().year,
                'Год издания не может быть больше текущего'
            )
        ]
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=False,
        null=True,
        verbose_name='Категория',
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='titles',
        verbose_name='Жанр',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = (
            'name',
        )

    def __str__(self):
        return self.name[:50]


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        blank=False,
        null=False
    )
    score = models.PositiveSmallIntegerField(
        blank=False,
        null=False
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_user_review'
            )
        ]

    def __str__(self):
        return self.text[:25]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        blank=False,
        null=False
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:25]
