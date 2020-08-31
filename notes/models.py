from django.db import models
from phone_field import PhoneField
# Create your models here.
from django.core.validators import MinValueValidator, RegexValidator

# from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Profile(models.Model):
	user=models.OneToOneField(User,on_delete=models.CASCADE)
	fullname=models.CharField(max_length=200,null=True)
	department=models.CharField(max_length=200,null=True)
	semester=models.IntegerField(null=True)
	rollno=models.IntegerField(null=True)
	phoneno=models.CharField(validators=[RegexValidator("^0?[5-9]{1}\d{9}$")], max_length=15, null=True, blank=True)
	gender=models.CharField(default="male",max_length=100,choices=(("male","male"),("female","female")))
	registrationno=models.IntegerField(null=True)
	profile_pic=models.ImageField(upload_to='images/',null=True)

	def __str__(self):

		return self.fullname


class Notes(models.Model):
	owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
	subject=models.CharField(max_length=200)
	course_code=models.CharField(max_length=200)
	file=models.FileField(upload_to='uploads/')
	credit=models.IntegerField(null=True)

	def __str__(self):

		return self.subject













