from django.urls import path
from notes.views import RegisterView,ApiRoot,LoginView,NoteUploadView,NoteDetailView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

	path('',ApiRoot.as_view()),
	path('register/',RegisterView.as_view(),name='register'),
	path('login/',LoginView.as_view(),name='login'),
	path('upload/',NoteUploadView.as_view(),name="upload"),
	path('note/<int:pk>/',NoteDetailView.as_view(),name="single-note")
	# path('login/',login,name="login"),

]


urlpatterns=format_suffix_patterns(urlpatterns)