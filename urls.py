from django.urls import path
from . import views

urlpatterns = [
    path('', views.drinks, name="drinks"),
    path('drink/<int:id>', views.drink, name="drink"),
    path('drink_list', views.DrinkList.as_view(), name="drink_list"),
    path('drink_rud/<int:pk>', views.DrinkRUD.as_view(), name="drink_rud"),
    path('signup', views.signup, name="signup"),
    path('login', views.login, name="login"),
    path('test_token', views.test_token, name="test_token"),
]