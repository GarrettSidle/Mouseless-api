from django.db import models
from django.contrib.auth.hashers import make_password
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