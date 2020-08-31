from django.urls import path
from notes.views import RegisterView,ApiRoot,LoginView,NoteUploadView,NoteDetailView,GlobalNoteSearch,GetMyNotes,ProfileView
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [

	path('',ApiRoot.as_view()),
	path('register/',RegisterView.as_view(),name='register'),
	path('login/',LoginView.as_view(),name='login'),
	path('upload/',NoteUploadView.as_view(),name="upload"),
	path('note/<int:pk>/',NoteDetailView.as_view(),name="single-note"),
	#list of all the notes of currently login user and also he/she can search with a username
	path('mynotes/',GetMyNotes.as_view(),name="mynotes"),

	#search all the notes with subject name uploaded by user except the current login in users
	path('list/',GlobalNoteSearch.as_view(),name="list"),
	path('profile/',ProfileView.as_view(),name="profile"),

	# path('^upload/(?P<subject>.+)/$', SearchNoteList.as_view(),name="search-note"),
	# path('login/',login,name="login"),

]


urlpatterns=format_suffix_patterns(urlpatterns)