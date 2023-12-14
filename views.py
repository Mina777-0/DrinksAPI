from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view
from .models import MyUser, Drink
from .serialisers import DrinkSerialisers, UserSerialiser
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny


class DrinkList(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerialisers
    authentication_classes= [TokenAuthentication, SessionAuthentication]
    permission_classes=[IsAuthenticatedOrReadOnly]

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request:Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    

class DrinkRUD(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    queryset = Drink.objects.all()
    serializer_class = DrinkSerialisers
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes=[IsAuthenticated]

    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request:Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request:Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)




@api_view(["GET","POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def drinks(request:Request):
    
    if request.method == "GET":
        drink= Drink.objects.all()
        serialiser = DrinkSerialisers(instance= drink, many= True)
        return Response(data= serialiser.data, status= status.HTTP_200_OK)
    
    if request.method == "POST":
        serialiser= DrinkSerialisers(data= request.data)
        if serialiser.is_valid():
            serialiser.save()
            response = {
                "message": "data is created successfully",
                "data": serialiser.data
            }
            return Response(data=response, status= status.HTTP_201_CREATED)
        return Response(data= serialiser.errors, status= status.HTTP_400_BAD_REQUEST)
    
@api_view(["GET", "PUT", "DELETE"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def drink(request:Request, id):
    drink = get_object_or_404(Drink, id= id)

    if request.method == "GET":
        serialiser = DrinkSerialisers(instance= drink)
        return Response(data= serialiser.data, status= status.HTTP_200_OK)

    if request.method == "PUT":
        serialiser = DrinkSerialisers(instance=drink, data= request.data)
        if serialiser.is_valid():
            serialiser.save()
            response = {
                "message": "data is updated successfully",
                "data": serialiser.data
            }
            return Response(data= response, status= status.HTTP_201_CREATED)
        return Response(data= serialiser.errors, status= status.HTTP_404_NOT_FOUND)

    if request.method == "DELETE":
        drink.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def signup(request:Request):
    serialiser = UserSerialiser(data= request.data)
    if serialiser.is_valid():
        serialiser.save()
        user = MyUser.objects.get(username= request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user = user)
        response= {"message": "User is created successfully",
                   "token": token.key,
                   "data": serialiser.data}
        return Response(data=response, status= status.HTTP_201_CREATED)
    return Response(data= serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@authentication_classes([TokenAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticatedOrReadOnly])
def login(request:Request):
    user = get_object_or_404(MyUser, username= request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"message": "User is Not Found"}, status= status.HTTP_404_NOT_FOUND)
    serialiser = UserSerialiser(instance=user)
    token, create = Token.objects.get_or_create(user= user)
    response= {
        "message":"User is Found",
        "token": token.key,
        "data": serialiser.data
    }

    return Response(data= response, status= status.HTTP_200_OK)


@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request:Request):
    return Response("passed for {}".format(request.user.username))
