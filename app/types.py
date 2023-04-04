from graphene_django.types import DjangoObjectType
from app.models import Fruit
from django.contrib.auth import get_user_model

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()

class FruitType(DjangoObjectType):
    class Meta:
        model = Fruit
