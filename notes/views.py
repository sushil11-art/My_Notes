from django.shortcuts import render
from notes.serializers import UserSerializer,LoginSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.reverse import reverse


from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny



# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
    serializer_class=LoginSerializer
    def post(self,request):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user=serializer.validated_data.get('user')
        user=serializer.validated_data['user']
        # user=validatedData['user']
        token,_=Token.objects.get_or_create(user=user)
        return Response({'token':token.key},status=status.HTTP_200_OK)


class ApiRoot(APIView):

    def get(self,request):

        return Response({

            'register':reverse('register',request=request),
            # 'hello':reverse('hello',request=request),

            'login':reverse('login',request=request),


        })


