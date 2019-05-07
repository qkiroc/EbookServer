from django.db import models

# Create your models here.
class user(models.Model):
	username = models.CharField(max_length = 20)
	sex = models.CharField(max_length = 1)
	signature = models.CharField(max_length = 200)
	password = models.CharField(max_length = 30)
	experience = models.CharField(max_length = 100)
	userhead = models.CharField(max_length = 100)

class book(models.Model):
	title = models.CharField(max_length = 100)
	btype = models.CharField(max_length = 20)
	author = models.CharField(max_length = 20)
	brief = models.TextField()

class concern(models.Model):
	concernuser = models.CharField(max_length = 10)
	concerneduser = models.CharField(max_length = 10)

class bookideal(models.Model):
	userid = models.CharField(max_length = 10)
	username = models.CharField(max_length = 20)
	userhead = models.CharField(max_length = 100)
	time = models.CharField(max_length = 100)
	content = models.TextField()
	quote = models.TextField()
	likecount = models.CharField(max_length = 100)

class like(models.Model):
	userid = models.CharField(max_length = 10)
	bookidealid = models.CharField(max_length = 100)

class comment(models.Model):
	userid = models.CharField(max_length = 10)
	username = models.CharField(max_length = 20)
	userhead = models.CharField(max_length = 100)
	bookidealid = models.CharField(max_length = 100)
	time = models.CharField(max_length = 100)
	coment = models.TextField()
		

		
		
		
