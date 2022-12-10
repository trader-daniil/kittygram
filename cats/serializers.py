from rest_framework import serializers
from .models import Cat, Achievement, COLOR_CHOICES
import datetime as dt
from django.contrib.auth.models import User


class AchievementSerializer(serializers.ModelSerializer):
    """Сериализатор для достижений кота."""
    id = serializers.IntegerField()

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
    #achievements = serializers.PrimaryKeyRelatedField(
    #    many=True,
    #    queryset=Achievement.objects.all(),
    #)
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
        read_only_fields = ('owner',)

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


    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.color = validated_data.get('color', instance.color)
        instance.birth_year = validated_data.get('birth_year', instance.birth_year)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()
        if 'achievements' not in validated_data.keys():
            instance.achievements.clear()
            return instance

        modified_achievements_ids = []
        achievements_data = validated_data.pop('achievements')
        for achievement_data in achievements_data:
            if 'id' not in achievement_data.keys():
                achievement = Achievement.objects.create(**achievement_data)
                achievement.cats.add(instance)
                modified_achievements_ids.append(achievement.id)
                continue

            achievement = Achievement.objects.get(id=achievement_data['id'])
            achievement.name = achievement_data.get('name', instance.name)
            if instance.id in achievement.cats.values_list('id', flat=True):
                achievement.save()
                modified_achievements_ids.append(achievement.id)
                continue
            achievement.cats.add(instance)
            achievement.save()
            modified_achievements_ids.append(achievement.id)
        for achievement in instance.achievements.all():
            if achievement.id in modified_achievements_ids:
                continue
            achievement.cats.remove(instance)
            achievement.save()
        return instance
            

class PersonSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""
    cats = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Cat.objects.all(),
        many=True,
    )

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'last_name',
            'sex',
            'cats',
        )
