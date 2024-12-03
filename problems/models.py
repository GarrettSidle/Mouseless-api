from django.db import models
from django.contrib.auth.models import User
import math

from enum import Enum

class StatisticType(Enum):
    Time = 1
    KeyStroke = 2
    Speed = 3


class Problem(models.Model):
    number = models.IntegerField(unique=True)  
    original_code_block = models.CharField(max_length=1028)
    modified_code_block = models.CharField(max_length=1028)
    
    def get_random_problem():
        """Return a random problem from the database."""
        return Problem.objects.order_by('?').first()
        


class Problem_Statistics(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    statistic_type = models.IntegerField(default=0)
    bin_index = models.IntegerField()
    value = models.DecimalField(default=0, decimal_places=2, max_digits=4)
    
    def update_stat(self, statistic_type, value):
        """Update the statistic for the problem."""
        stat, created = Problem_Statistics.objects.get_or_create(
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
            stat = Problem_Statistics.objects.get(
                problem=self.problem, 
                statistic_type=statistic_type, 
            )
            return stat.value
        except Problem_Statistics.DoesNotExist:
            return None
    
class User_Problem_Statistics(models.Model):
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
        stat, created = User_Problem_Statistics.objects.get_or_create(user=user, problem=problem)
        return stat
