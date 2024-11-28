from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
import math

from enum import Enum

class StatisticType(Enum):
    Time = 1
    KeyStroke = 2
    Speed = 3

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
    
    def get_random_problem():
        """Return a random problem from the database."""
        return Problem.objects.order_by('?').first()
        


class ProblemStatistics(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    statistic_type = models.IntegerField(default=0)
    bin_index = models.IntegerField()
    value = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    
    def update_stat(self, statistic_type, value):
        """Update the statistic for the problem."""
        stat, created = ProblemStatistics.objects.get_or_create(
            problem=self.problem, 
            statistic_type=statistic_type, 
        )
        match(statistic_type):
            case StatisticType.Time: 
                stat.bin_index = math.floor(value / 5)
            case StatisticType.KeyStroke:
                stat.bin_index = math.floor(value / 3)
            case StatisticType.Speed:
                stat.bin_index = math.floor(value / 25)
        
        stat.value = value
        stat.save()
        return stat
    
    def get_stat(self, statistic_type, bin_index):
        """Retrieve the statistic for the given problem."""
        try:
            stat = ProblemStatistics.objects.get(
                problem=self.problem, 
                statistic_type=statistic_type, 
            )
            return stat.value
        except ProblemStatistics.DoesNotExist:
            return None
    
class UserProblemStatistics(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    best_time = models.DecimalField(default=0, decimal_places=2, max_digits=4) 
    best_key_strokes = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    best_speed = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    
    def get_best_times(self):
        """Retrieve the best time for a user on a specific problem."""
        return self.best_time

    def update_best_time(self, new_time):
        """Update the user's best time for this problem."""
        if new_time < self.best_time or self.best_time == 0:
            self.best_time = new_time
            self.save()
    
    def update_best_key_strokes(self, new_key_strokes):
        """Update the user's best key strokes for this problem."""
        if new_key_strokes < self.best_key_strokes or self.best_key_strokes == 0:
            self.best_key_strokes = new_key_strokes
            self.save()
    
    def update_best_speed(self, new_speed):
        """Update the user's best speed for this problem."""
        if new_speed > self.best_speed or self.best_speed == 0:
            self.best_speed = new_speed
            self.save()

    def create_new_problem_stat(self, user, problem):
        """Create a new UserProblemStatistics entry."""
        stat, created = UserProblemStatistics.objects.get_or_create(user=user, problem=problem)
        return stat
    
    
class Session(models.Model):
    session_key = models.CharField(max_length=40, unique=True)  
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  
    created_at = models.DateTimeField(auto_now_add=True)  
    last_accessed = models.DateTimeField(auto_now=True) 
    expires_at = models.DateTimeField(default=timezone.now() + timedelta(days=3))
    
    def create_session_key(self, user):
        """Create a new session key for the user."""
        from django.utils.crypto import get_random_string
        self.session_key = get_random_string(40)
        self.user = user
        self.save()
    
    def delete_session_key(self):
        """Delete the session key."""
        self.delete()

    def check_session_key(self):
        """Check if the session has expired."""
        if self.expires_at > timezone.now():
            return True
        return False

    def reset_expiration(self):
        """Reset the session expiration to 3 days from now."""
        self.expires_at = timezone.now() + timedelta(days=3)
        self.save()