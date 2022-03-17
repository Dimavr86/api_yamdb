import datetime as dt

from django.core.validators import MaxValueValidator
from django.db import models


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