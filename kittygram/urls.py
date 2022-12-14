from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token


from .views import (
    PersonViewSet,
    get_or_create_cats,
    greet,
    get_or_update_or_delete_cat,
    ListCats,
    CatDetail,
    ListCats2,
    CatDetail2,
    CatViewSet,
    AchievementViewSet,
)

router = DefaultRouter()
router.register(
    prefix='cats4',
    viewset=CatViewSet,
    basename='cats',
)
router.register(
    prefix='persons',
    viewset=PersonViewSet,
    basename='persons',
)
router.register(
    prefix='achievements',
    viewset=AchievementViewSet,
    basename='achievements',
)

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('cats/', get_or_create_cats),
    #path('greet_page/', greet),
    #path('cats/<int:cat_id>', get_or_update_or_delete_cat),
    #path('cats2/', ListCats.as_view()),
    #path('cats2/<int:cat_id>', CatDetail.as_view()),
    #path('cats3/', ListCats2.as_view()),
    #path('cats3/<int:cat_id>', CatDetail2.as_view()),
    path('', include(router.urls)),
    #path('api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
