from rest_framework import serializers
from .models import Cat

class CatSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Cat."""
    
    class Meta:
        model = Cat
        fields = (
            'id',
            'name',
            'birth_year',
        )