from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import validate_email, validate_me, validate_username


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'author', 'title', 'text', 'score', 'pub_date')
        read_only_fields = ('author', 'title',)

    def validate_score(self, value):
        if not (1 <= value <= 10):
            raise serializers.ValidationError('Недопустимая оценка!')
        return value

    def validate(self, data):
        if self.context['request'].method == 'POST':
            current_user = self.context['request'].user
            title_id = self.context['view'].kwargs.get(['title_id'][0])
            title = get_object_or_404(Title, id=title_id)
            is_review_already_exist = title.reviews.filter(
                author=current_user
            )
            if is_review_already_exist:
                raise serializers.ValidationError(
                    'Отзыв на это произведение уже существует!'
                )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'review',)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleWriteSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
        required=False
    )
    rating = serializers.IntegerField(
        max_value=10,
        min_value=1,
        read_only=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category',
                  'genre', 'description', 'rating',)


class TitleReadSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(
        max_value=10,
        min_value=1,
        read_only=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'category',
                  'genre', 'description', 'rating',)
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        validators=[validate_email]
    )
    username = serializers.CharField(
        max_length=150,
        validators=[validate_username]
    )

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class RegUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    username = serializers.CharField(validators=[validate_me])

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if (
            User.objects.filter(email=email).exists()
            and User.objects.get(email=email).username != username
        ):
            raise ValidationError('Укажите имя Пользователя')

        if (
            User.objects.filter(username=username).exists()
            and User.objects.get(username=username).email != email
        ):
            raise ValidationError('Укажите электронную почту')

        return data

    class Meta:
        model = User
        fields = ('username', 'email')


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)

        if user is None:
            raise serializers.ValidationError(
                'Некорректный Пользователь'
            )

        if confirmation_code is None:
            raise serializers.ValidationError(
                'Некорректный или устаревший код'
            )

        return data
