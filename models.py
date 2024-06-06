from django.db import models
from django.contrib.auth.models import User

class Blog(models.Model):
    TYPE=(
        ('LifeStyle','LifeStyle'),
        ('Business','Business'),
        ('Fashion','Fashion'),
        ('Travel','Travel')
    )
    title=models.CharField(max_length=50)
    content=models.CharField(max_length=50)
    image=models.ImageField(upload_to='images/')
    type=models.CharField(max_length=50,choices=TYPE)

class Comment(models.Model):
    fk_user=models.ForeignKey(User,on_delete=models.CASCADE)
    fk_blog= models.ForeignKey(Blog, on_delete=models.CASCADE)
    comment= models.TextField()

class Profile(models.Model):
    user= models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=10)
    location=models.CharField(max_length=50)
    photo=models.ImageField (upload_to='profile_pic/')

class Otp(models.Model):
    fk_user=models.OneToOneField(User,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)

    
