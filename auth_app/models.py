from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # Store hashed password
    created_at = models.DateTimeField(auto_now_add=True)   # Store the creation date

    def set_password(self, raw_password):
        """Hashes the password before saving it"""
        self.password = make_password(raw_password)
    
    def authenticate(self, raw_username, raw_password):
        try:
            user = User.objects.get(username=raw_username)  
            if check_password(raw_password, user.password): 
                return user 
            return None  
        except ObjectDoesNotExist:
            return None 
    
        

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
        
        #if the user already has a key
        try:
            #get existing sessions
            session = Session.objects.get(user=user)
            
            #if session is not expired
            if(session.expires_at > timezone.now()):
                #reset expiration and return it to user
                session.reset_expiration()
                return session
            #if it is expired, delete the key
            session.delete_session_key()
            session = None
            
        except Session.DoesNotExist:
            session = None
            
        #create a new key and add it to the db
        session = Session.objects.create(session_key=get_random_string(40), user=user)
        session.save()
        return session
    
    def delete_session_key(self):
        """Delete the session key."""
        self.delete()

    def check_session_key(raw_session_key: str):
        """Check if the session has expired."""
        print(raw_session_key)
        try:
            session = Session.objects.get(session_key=raw_session_key)
            if session.expires_at > timezone.now():
                return True
            session.delete_session_key()
        except: 
            return False

    def reset_expiration(self):
        """Reset the session expiration to 3 days from now."""
        self.expires_at = timezone.now() + timedelta(days=3)
        self.save()