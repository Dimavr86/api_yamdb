from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole():
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLES = (
        (USER, 'Пользователь с паролем'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Админ'),
    )

    LEN_ROLES = max(len(i[0]) for i in ROLES)


class User(AbstractUser):

    username = models.CharField('Имя Пользователя', max_length=150,
                                unique=True, blank=False, null=False)
    email = models.EmailField('Email пользователя', max_length=254,
                              unique=True, blank=False, null=False)
    role = models.CharField('Роль пользователя',
                            max_length=UserRole.LEN_ROLES,
                            choices=UserRole.ROLES,
                            default=UserRole.USER)
    bio = models.TextField('О пользователе', blank=True,)
    first_name = models.CharField('Имя', max_length=150, blank=True)
    last_name = models.CharField('Фамилия', max_length=150,
                                 blank=True)

    class Meta:
        ordering = ('role',)

    @property
    def is_user(self):
        return self.role == UserRole.USER

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    @property
    def is_admin(self):
        return (self.role == UserRole.ADMIN
                or self.is_staff)
