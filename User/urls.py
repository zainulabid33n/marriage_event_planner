from django.urls import include, path
from rest_framework.routers import DefaultRouter

from User import views

router = DefaultRouter()
# router.register(r'test', views.TestView, basename='test'),
router.register(r'user/signup', views.UserSignup, basename='UserSignup'),
router.register(r'user', views.UserView, basename='MyUsers'),


urlpatterns = [
    path('', include(router.urls)),
    path('api/login', views.LoginView.as_view({'get': 'post'})),
]
