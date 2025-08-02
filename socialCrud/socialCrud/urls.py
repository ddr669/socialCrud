
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views as views_
from django.contrib import admin 
from socialCrud.quickstart import views
from front_end import views as _views


router = routers.DefaultRouter()

router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'home', views.HomePageViewSet)
#router.register(r'homepage', _views.HomePageMain, basename='homepage')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-api-auth/', views_.obtain_auth_token),
    path('homepage/', _views.HomePageMain),
    path('register/', _views.UserRegister),
    path('login/', _views.LoginUser),
    path('logout/', _views.logOut),
]