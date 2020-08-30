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
	parser_class=(FileUploadParser,)

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

	# get all notes
	def get(self,request,format=None):
		notes=Notes.objects.filter(owner=request.user.profile)
		serializer=NoteSerializer(notes,many=True)
		return Response(serializer.data)


	
class NoteDetailView(APIView):
	permission_classes=[permissions.IsAuthenticated]
	parser_class=(FileUploadParser,)
	# check whether note exist or not 
	def get_object(self,pk,format=None):
		try:
			return Notes.objects.filter(pk=pk).first()

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
		serializer=NoteSerializer(note,data=request.data)
		if serializer.is_valid():
			serializer.save(owner=request.user.profile)
			return Response(serializer.data)

		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	# delete one particular
	def delete(self,request,pk,format=None):
		note=self.get_object(pk)
		note.delete()
		return Response(status=status.HTTP_200_OK)

	

class ApiRoot(APIView):

    def get(self,request,format=None):

        return Response({

            'register':reverse('register',request=request,format=format),
            # 'hello':reverse('hello',request=request),

            'login':reverse('login',request=request,format=format),
            'upload':reverse('upload',request=request,format=format),


        })


