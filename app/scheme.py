import graphene
from app.models import Fruit
from .types import UserType, FruitType
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required
import graphql_jwt

User = get_user_model()

class Query:
    current_user = graphene.Field(UserType)
    all_users = graphene.List(UserType)

    fruit= graphene.Field(FruitType, id=graphene.Int())
    all_fruits = graphene.List(FruitType)

    def resolve_current_user(root, info):
        user = info.context.user
        return user

    @login_required
    def resolve_all_users(root, info):
        return User.objects.all()

    @login_required
    def resolve_fruit(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Fruit.objects.get(pk=id)
        return None

    @login_required
    def resolve_all_fruits(self, info, **kwargs):
        return Fruit.objects.all()

class CreateUserMutation(graphene.Mutation):
    success = graphene.Boolean()
    message = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password1 = graphene.String(required=True)
        password2 = graphene.String(required=True)

    def mutate(self, info, username, email, password1, password2):
        existsUsername = User.objects.filter(username=username).exists()
        if existsUsername:
            return CreateUserMutation(success=False, message="登録済みのユーザーIDです", user=None)

        existsEmail = User.objects.filter(email=email).exists()
        if existsEmail:
            return CreateUserMutation(success=False, message="登録済みのメールアドレスです", user=None)

        errorPassword = password1 != password2
        if errorPassword:
            return CreateUserMutation(success=False, message="パスワードが一致していません", user=None)

        user = get_user_model()(
            username=username,
            email=email,
        )

        user.set_password(password1)
        user.save()

        return CreateUserMutation(success=True, message="アカウント登録に成功しました", user=user)

class CreateFruitMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        color = graphene.String(required=True)

    fruit = graphene.Field(FruitType)

    def mutate(self, info, name, color):
        fruit = Fruit.objects.create(name=name, color=color)
        return CreateFruitMutation(fruit=fruit)

class UpdateFruitMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        color = graphene.String()
        id = graphene.ID(required=True)

    fruit = graphene.Field(FruitType)

    def mutate(self, info, name, color, id):
        fruit = Fruit.objects.get(id=id)
        fruit.name = name
        fruit.color = color
        fruit.save()
        return UpdateFruitMutation(fruit=fruit)

class DeleteFruitMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    fruit = graphene.Field(FruitType)

    def mutate(self, info, id):
        fruit = Fruit.objects.get(id=id)
        fruit.delete()
        return DeleteFruitMutation()

class Mutation(graphene.ObjectType):
    create_user = CreateUserMutation.Field() # ユーザー登録
    token_auth = graphql_jwt.ObtainJSONWebToken.Field() # トークン生成
    verify_token = graphql_jwt.Verify.Field() # トークン認証
    refresh_token = graphql_jwt.Refresh.Field() # トークン再生成
    revoke_token = graphql_jwt.Revoke.Field() # リフレッシュトークン無効化

    create_fruit = CreateFruitMutation.Field()
    update_fruit = UpdateFruitMutation.Field()
    delete_fruit = DeleteFruitMutation.Field()
