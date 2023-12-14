from rest_framework import serializers
from .models import Drink, MyUser

class DrinkSerialisers(serializers.ModelSerializer):
    class Meta:
        model= Drink
        fields= "__all__"

class UserSerialiser(serializers.ModelSerializer):
    class Meta:
        model= MyUser
        fields = ["email", "first_name", "last_name", "username", "password"]