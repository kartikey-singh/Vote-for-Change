from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# import datetime
# from django.utils import timezone
# Create your models here.
class UserProfile(models.Model):
	user = models.OneToOneField(User, primary_key=True)
	def __str__(self):
		return '%s-%s' %(self.user.first_name, self.user.last_name)

class Cause(models.Model):
	causeId = models.AutoField(primary_key = True)
	name = models.CharField(max_length=50)
	# user = models.ForeignKey(User,null=True)
	# activeStatus = models.BooleanField(default=False)    
	# submitStatus = models.BooleanField(default=False)    
	# description = models.TextField(null = True) 
	def __str__(self):
		return 'Name : %s -- Poll ID: %s  ' %(self.name,self.causeId)

class Vote(models.Model):
	voteId = models.AutoField(primary_key = True)
	cause = models.ForeignKey(Cause,null=True)
	user = models.ForeignKey(User,null=True)
	activeStatus = models.BooleanField(default=False)
	submitStatus = models.BooleanField(default=False)    
	def __str__(self):
		return 'Vote ID: %s -- Poll Submit: %s -- Answer Submit: %s' %(self.voteId,self.activeStatus, self.submitStatus)


		
# -- Poll Submit %s -- Answer Submit %s self.activeStatus, self.submitStatus
# class Vote(models.Model):
# 	cause = models.ForeignKey(Cause,null=True)
# 	user = models.ForeignKey(User,null=True)
# 	voteId = models.AutoField(primary_key = True)
# 	activeStatus = models.BooleanField(default=False)    
# 	submitStatus = models.BooleanField(default=False)    
# 	def __str__(self):
# 		return 'Vote ID: %s -- Poll Submit %s -- Answer Submit %s ' %(self.voteId, self.activeStatus, self.submitStatus)
# class VoteData(object): object creation
# 	responseId = models.AutoField(primary_key = True)
# 	quiz = models.ForeignKey(Quiz,null=True)
# 	user = models.ForeignKey(User,null=True)
# 	timeOfAttempt = models.DateTimeField(null = True)
# 	activeStatus = models.BooleanField(default=True)
# 	def __str__(self):
# 		return '%s - %s' %(self.user.email, self.quiz)	
					