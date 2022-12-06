from rest_framework import serializers
from .models import Cat, Person, Achievement, COLOR_CHOICES
import datetime as dt


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
            return instance

        achievements_data = validated_data.pop('achievements')
        for achievement_data in achievements_data:
            if 'id' in achievement_data.keys():
                achievement = Achievement.objects.get(id=achievement_data['id'])
                achievement.name = achievement_data.get('name', instance.name)
                achievement.save()
                continue

            achievement = Achievement.objects.create(**achievement_data)
            achievement.cats.add(instance)
        return instance
            
            
        
            

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
