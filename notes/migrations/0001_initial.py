# Generated by Django 3.1 on 2020-08-30 04:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phone_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fullname', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('semester', models.IntegerField()),
                ('rollno', models.IntegerField()),
                ('phoneno', phone_field.models.PhoneField(blank=True, max_length=31)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=100)),
                ('registrationno', models.IntegerField()),
                ('profile_pic', models.ImageField(null=True, upload_to='images/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=200)),
                ('course_code', models.CharField(max_length=200)),
                ('file', models.FileField(upload_to='uploads/')),
                ('credit', models.IntegerField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='notes.profile')),
            ],
        ),
    ]
