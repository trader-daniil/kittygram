from rest_framework import serializers
from .models import Cat, Person, Achievement, COLOR_CHOICES
import datetime as dt


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор для достижений кота."""

    class Meta:
        model = Achievement
        fields = (
            'id',
            'name',
        )


class CatListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка всех котов."""
    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'color',
        )

class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cat."""
    achievements = AchievementSerializer(
        many=True,
        #read_only=True,
        required=False,
    )
    age = serializers.SerializerMethodField()
    inscription = serializers.SerializerMethodField()
    color = serializers.ChoiceField(choices=COLOR_CHOICES)


    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'birth_year',
            'owner',
            'achievements',
            #'get_age',
            'age',
            'inscription',
            'color',
        )

    def get_age(self, obj):
        return dt.datetime.now().year - obj.birth_year

    def get_inscription(self, obj):
        return 'Simple inscription'


    def create(self, validated_data):
        if 'achievements' not in validated_data:
            cat = Cat.objects.create(**validated_data)
            return cat

        achievements_data = validated_data.pop('achievements')
        cat = Cat.objects.create(**validated_data)
        for achievement_data in achievements_data:
            achievement, _ = Achievement.objects.get_or_create(**achievement_data)
            achievement.cats.add(cat)
        return cat


class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Person."""
    cats = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Cat.objects.all(),
        many=True,
    )

    class Meta:
        model = Person
        fields = (
            'id',
            'first_name',
            'last_name',
            'sex',
            'cats',
        )
