from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cats.models import Cat
from cats.serializers import CatSerializer


@api_view(['GET', 'POST'])
def get_or_create_cats(request):
    """
    Получаем всех котов или создаем нового.
    """
    if request.method == 'POST':
        serialized_cat = CatSerializer(data=request.data)
        if not serialized_cat.is_valid():
            return Response(serialized_cat.errors, status=status.HTTP_400_BAD_REQUEST)
        serialized_cat.save()
        return Response(serialized_cat.data, status=status.HTTP_201_CREATED)

    cats = Cat.objects.all()
    serialized_cats = CatSerializer(
        cats,
        many=True,
    )
    return Response(serialized_cats.data)