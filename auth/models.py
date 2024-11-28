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