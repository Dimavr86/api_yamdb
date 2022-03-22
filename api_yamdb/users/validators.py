from rest_framework.exceptions import ValidationError

from .models import User


def validate_username(value):
    if value == 'me':
        raise ValidationError('Выберите другое имя')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('Такое имя уже зарегистрировано!')


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Такая почта уже используется')
