from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone

class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)   # Store the creation date

    def set_password(self, raw_password):
        """Hashes the password before saving it"""
        self.password = make_password(raw_password)
    
    def check_password(self, raw_password):
        """Checks if the raw password matches the hashed one"""
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username

class Problem(models.Model):
    number = models.IntegerField(unique=True)  
    original_code_block = models.CharField(max_length=1028)
    modified_code_block = models.CharField(max_length=1028)


class ProblemStatistics(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    statistic_type = models.IntegerField(default=0)
    bin_index = models.IntegerField()
    value = models.DecimalField(default=0)
    
class UserProblemStatistics(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    best_time = models.DecimalField(default=0) 
    best_key_strokes = models.DecimalField(default=0)
    best_speed = models.DecimalField(default=0)
    
class Session(models.Model):
    session_key = models.CharField(max_length=40, unique=True)  
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  
    created_at = models.DateTimeField(auto_now_add=True)  
    last_accessed = models.DateTimeField(auto_now=True) 
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=3))