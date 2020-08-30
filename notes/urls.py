from django.urls import path
from notes.views import RegisterView,ApiRoot,LoginView
urlpatterns = [

	path('',ApiRoot.as_view()),
	path('register/',RegisterView.as_view(),name='register'),
	path('login/',LoginView.as_view(),name='login'),
	# path('login/',login,name="login"),

]
