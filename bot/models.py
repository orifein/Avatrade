from django.db import models
from django.contrib.admin.utils import flatten

# Create your models here.


class User(models.Model):
    
    user_id = models.Field(primary_key=True)
    email = models.CharField(max_length=200)
    password =  models.CharField(max_length=200)
    name = models.CharField(max_length=200, null=True)


    def __str__(self):
        return str(self.user_id)


class Post(models.Model):

    post_id = models.Field(primary_key=True)
    user_id = models.IntegerField()
    title =  models.CharField(max_length=200)


    def __str__(self):
        return str(self.post_id)



class Like(models.Model):

    post_id = models.IntegerField()
    like_by_user_id = models.IntegerField()


    def __str__(self):
        return str(self.post_id)
