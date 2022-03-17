from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    user = 'user'
    moderator = 'moderator'
    admin = 'admin'

    role_list = (
        (user, 'Пользователь с паролем'),
        (moderator, 'Модератор'),
        (admin, 'Админ'),
    )

    bio = models.TextField('Сведения о пользователе', blank=True,)
    role = models.CharField('Роль пользователя', max_length=40,
                            choices=role_list, default='user')

    class Meta:
        ordering = ('role',)

    @property
    def is_user(self):
        return self.role == User.user

    @property
    def is_moderator(self):
        return self.role == User.moderator

    @property
    def is_admin(self):
        return self.role == User.admin

