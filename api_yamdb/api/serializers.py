import datetime as dt

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers

from reviews.models import Category, Comments, Genres, Title, Review
from users.models import User


class UserCreateSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    email = serializers.EmailField(
        max_length=150,
        required=True
    )

    class Meta:
        model = User
        fields = (
            'username', 'email'
        )

    def validate(self, data):
        email = data.get('email')
        username = data.get('username')

        if data.get('username') == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" запрещено'
            )
        if not User.objects.filter(username=username, email=email).exists():
            if User.objects.filter(username=username).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким именем уже существует'
                )
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError(
                    'Пользователь с таким email уже существует'
                )
        return data


class UserRecieveTokenSerializer(serializers.Serializer):
    username = serializers.RegexField(
        regex=r'^[\w.@+-]+$',
        max_length=150,
        required=True
    )
    confirmation_code = serializers.CharField(
        max_length=150,
        required=True
    )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует')
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genres


class TitleGetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        fields = (
            "id",
            "name",
            "year",
            "rating",
            "description",
            "genre",
            "category")
        model = Title

    def get_rating(self, obj):
        return obj.reviews.aggregate(Avg('score'))['score__avg']


class TitlePostSerializer(serializers.ModelSerializer):
    """Сериализатор для POST-запросов к произведениям."""

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genres.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

    def validate_year(self, value):
        year = dt.date.today().year
        if year < value:
            raise serializers.ValidationError(
                'Это произведение еще не вышло!')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ("id", "text", "pub_date", "score", "author")
        read_only_fields = ('title',)

    def validate(self, data):
        title_id = self.context['request'].parser_context['kwargs']['title_id']
        title = get_object_or_404(Title, id=title_id)
        if "POST" in str(self.context['request']):
            for obj in title.reviews.all():
                if obj.author == self.context['request'].user:
                    raise serializers.ValidationError(
                        "Вы уже написали отзыв к данному произведению")
        return data


class CommentsSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comments
        read_only_fields = ('review',)
