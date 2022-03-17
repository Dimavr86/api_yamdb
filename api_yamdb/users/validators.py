from rest_framework.exceptions import ValidationError

from .models import User


def validate_username(value):
    if value == 'me':
        raise ValidationError('Вы уже назвались этим именем')
    elif User.objects.filter(username=value).exists():
        raise ValidationError('Имя уже занято')

def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise ValidationError('Такая почта уже используется')
