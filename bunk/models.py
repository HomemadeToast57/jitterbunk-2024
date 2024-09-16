from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

class UserManager(BaseUserManager):
    def create_user(self, username, photo, password=None):
        """
        Creates and saves a User with the given username, photo, and password.
        """
        
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            photo=photo,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, photo, password):
        """
        Creates and saves a superuser with the given username, photo, and password.
        """
        user = self.create_user(
            username=username,
            photo=photo,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    photo = models.URLField(max_length=500, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['photo']

    def __str__(self):
        return self.username

class Bunk(models.Model):
    from_user = models.ForeignKey(User, related_name='bunks_sent', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='bunks_received', on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bunk from {self.from_user} to {self.to_user} at {self.time}"