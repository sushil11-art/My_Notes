from django.shortcuts import render
from notes.serializers import UserSerializer,LoginSerializer,NoteSerializer
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView
from rest_framework.reverse import reverse



from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import AllowAny


from rest_framework import viewsets
from rest_framework.parsers import FileUploadParser,MultiPartParser
from rest_framework import permissions

from notes.models import Notes

from django.http import Http404


#Paginator and filter
from django.core.paginator import Paginator

from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from notes.permissions import IsOwnerOrReadOnly

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
    def post(self,request,format=None):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # user=serializer.validated_data.get('user')
        user=serializer.validated_data['user']
        # user=validatedData['user']
        token,_=Token.objects.get_or_create(user=user)
        return Response({'token':token.key},status=status.HTTP_200_OK)

class NoteUploadView(APIView):
	permission_classes=[permissions.IsAuthenticated]
	authentication_classes=(TokenAuthentication,)

	parser_class=(FileUploadParser,)
	filter_backends=[filters.SearchFilter]
	search_fields=['subject']

    # filter_backends=[DjangoFilterBackend]
	# create notes
	def post(self,request,format=None):
		serializer=NoteSerializer(data=request.data)
		#another method of saving 
		# serializer.is_valid(raise_exception=True)
		# serializer.save(owner=request.user.profile)
		# return Response(serializer.data,status=status.HTTP_201_CREATED)
		if serializer.is_valid():
			serializer.save(owner=request.user.profile)
			return Response(serializer.data,status=status.HTTP_201_CREATED)

		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class GetMyNotes(generics.ListAPIView):
	permission_classes=[permissions.IsAuthenticated]
	authentication_classes=(TokenAuthentication,)
	serializer_class=NoteSerializer
	filter_backends=[filters.SearchFilter]
	search_fields=['subject']
	def get_queryset(self):
		notes=Notes.objects.filter(owner=self.request.user.profile)
		return notes

	#  get all the notes of currently login user with custom paggination

	# get all notes
	# def get(self,request,format=None):
	# 	notes=Notes.objects.all()
	# 	# notes=Notes.objects.filter(owner=request.user.profile)
	# 	# include paginator 
	# 	page_number=self.request.query_params.get('page_number',1)
	# 	page_size=self.request.query_params.get('page_size',10)
	# 	paginator=Paginator(notes,page_size)
	# 	# serializer=NoteSerializer(notes,many=True)
	# 	serializer=NoteSerializer(paginator.page(page_number),many=True)

	# 	return Response(serializer.data,status=status.HTTP_200_OK)

class GlobalNoteSearch(generics.ListAPIView):
	permission_classes=[permissions.IsAuthenticated]
	authentication_classes=(TokenAuthentication,)
	serializer_class=NoteSerializer
	filter_backends=[filters.SearchFilter]
	search_fields=['subject']
	def get_queryset(self):
		notes=Notes.objects.exclude(owner=self.request.user.profile)
		return notes

# with generic view to check whether a user has a permissin for a particular action

# class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
# 	permission_classes=[permissions.IsAuthenticated]
# 	authentication_classes=(TokenAuthentication,)
# 	parser_class=(FileUploadParser,)
# 	serializer_class=NoteSerializer
# 	def get_queryset(self):
# 		return Notes.objects.filter(owner=self.request.user.profile)


# my own flow to check whether a user has permission or note while i am writing custom view

class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
	permission_classes=[permissions.IsAuthenticated,IsOwnerOrReadOnly]
	authentication_classes=(TokenAuthentication,)
	parser_class=(FileUploadParser,)
	# check whether note exist or not 
	def get_object(self,pk,format=None):
		try:
			return Notes.objects.get(pk=pk)
		except Notes.DoesNotExist:
			raise Http404
	# get one single note
	def get(self,request,pk,format=None):
		print(pk)
		note=self.get_object(pk)
		serializer=NoteSerializer(note)
		return Response(serializer.data)
	# update one particular note
	def put(self,request,pk,format=None):
		note=self.get_object(pk)
		self.check_object_permissions(request,note)
		serializer=NoteSerializer(note,data=request.data)
		if serializer.is_valid():
			serializer.save(owner=request.user.profile)
			return Response(serializer.data)

		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	# delete one particular
	def delete(self,request,pk,format=None):
		note=self.get_object(pk)
		self.check_object_permissions(request,note)
		note.delete()
		return Response({"message":"successfully deleted"},status=status.HTTP_200_OK)


class ApiRoot(APIView):

    def get(self,request,format=None):

        return Response({

            'register':reverse('register',request=request,format=format),
            # 'hello':reverse('hello',request=request),

            'login':reverse('login',request=request,format=format),
            'upload':reverse('upload',request=request,format=format),
            'list':reverse('list',request=request,format=format),
            'mynotes':reverse('mynotes',request=request,format=format),


        })


