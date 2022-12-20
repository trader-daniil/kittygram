from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from cats.models import Cat, Achievement
from cats.serializers import (
    CatSerializer,
    PersonSerializer,
    CatListSerializer,
    CreateAchievementSerializer,
)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny


class AchievementViewSet(viewsets.ModelViewSet):
    """Операции CRUD с моделью Achievement."""
    queryset = Achievement.objects.all()
    serializer_class = CreateAchievementSerializer
    permission_classes = (AllowAny,)


class PersonViewSet(viewsets.ModelViewSet):
    """
    Операции CRUD с моделью Person.
    """
    queryset = User.objects.all()
    serializer_class = PersonSerializer


class CatViewSet(viewsets.ModelViewSet):
    """
    Операции CRUD с моделью Cat.
    """
    queryset = Cat.objects.all()
    serializer_class = CatSerializer

    @action(detail=False, url_path='white-cats')
    def get_white_cats(self, request):
        print(request.user.username)
        white_cats = Cat.objects.filter(color='White')
        serializer = self.get_serializer(white_cats, many=True)
        return Response(serializer.data)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CatListSerializer
        return CatSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ListCats2(generics.ListCreateAPIView):
    """
    Получение и создание котов.
    """
    queryset = Cat.objects.all()
    serializer_class = CatSerializer


class CatDetail2(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление и удаление одного объекта.
    """
    queryset = Cat.objects.all()
    serializer_class = CatSerializer
    lookup_url_kwarg = 'cat_id'
    lookup_field = 'pk'


class ListCats(APIView):
    """
    Получение всех котов или создание нового.
    """
    def get(self, request, format=None):
        """
        Получаем всех котов.
        """
        cats = Cat.objects.all()
        serialized_cats = CatSerializer(
            cats,
            many=True,
        )
        return Response(serialized_cats.data)


    def post(self, request, format=None):
        """
        Создание нового поста или нескольких постов.
        """
        serialized_cat = CatSerializer(
            data=request.data,
            many=True,
        )
        if not serialized_cat.is_valid():
            return Response(
                serialized_cat.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        serialized_cat.save()
        return Response(
            serialized_cat.data,
            status=status.HTTP_201_CREATED,
        )



class CatDetail(APIView):
    """
    Получение, обновление и удаление кота.
    """
    def get_cat(self, cat_id):
        try:
            return Cat.objects.get(pk=cat_id)
        except Cat.DoesNotExist:
            raise Http404

    def get(self, request, cat_id, format=None):
        cat = self.get_cat(cat_id)
        serialized_cat = CatSerializer(cat)
        return Response(serialized_cat.data)

    def put(self, request, cat_id, format=None):
        cat = self.get_cat(cat_id)
        serialized_cat = CatSerializer(
            cat,
            data=request.data,
            partial=True,
        )
        if serialized_cat.is_valid():
            serialized_cat.save()
            return Response(serialized_cat.data)
        return Response(
            serialized_cat.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, cat_id, format=None):
        cat = self.get_cat(cat_id)
        cat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET', 'POST'])
def get_or_create_cats(request):
    """
    Получаем всех котов или создаем нового.
    """
    if request.method == 'POST':
        serialized_cat = CatSerializer(
            data=request.data,
            many=True,
        )
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


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_or_update_or_delete_cat(request, cat_id):
    """
    Получаем кота по его id, затем возвращаем кота или обновляем или удаляем.
    """
    cat = Cat.objects.get(id=cat_id)
    if request.method == 'GET':
        serialized_cat = CatSerializer(cat)
        return Response(serialized_cat.data)
    elif request.method == 'PUT' or request.method == 'PATCH':
        serialized_cat = CatSerializer(
            cat,
            data=request.data,
            partial=True,
        )
        if serialized_cat.is_valid():
            serialized_cat.save()
            return Response(status=status.HTTP_201_CREATED)
        
    cat.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['GET', 'POST'])
def greet(request):
    """
    Приветсвуем на GET запрос и возвращаем переданные в теле данные на POST запрос
    """
    if request.method == 'POST':
        return Response(
            {
                'message': 'Получены данные',
                'data': request.data,
            },
        )
    return Response(
        {'message': 'Это был GET запрос!'}
    )
