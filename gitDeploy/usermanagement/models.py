from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
import hashlib

class AccountManager(BaseUserManager):
    def create_user(self, username, password=None, **kwargs):
        if not username:
            raise ValueError('User must have a valid username!') 
        
        if not kwargs.get('email'):
            raise ValueError('User must have a valid email!')
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        encoded = (timestamp + kwargs.get('email')).encode('utf-8')
        uid = kwargs.get('role', 'u')+"-"+hashlib.sha256(encoded).hexdigest()

        account = self.model(
            email=self.normalize_email(kwargs.get('email')),
            username=username,
            firstname=kwargs.get('firstname', None),
            lastname=kwargs.get('lastname', None),
            role=kwargs.get('role', 'u'),
            uid=uid
        )

        account.set_password(password)
        account.save()

        return account()
    
    def create_superuser(self, username, password=None, **kwargs):
        account = self.create_user(username, password, kwargs)
        account.is_admin = True
        account.save()

        return account

class Account(AbstractBaseUser):
    ROLES = (
        ('u', 'User'),
        ('m', 'Manager'),
        ('a', 'Administrator')
    )

    username = models.CharField(unique=True, max_length=255)
    email = models.EmailField(unique=True)

    firstname = models.CharField(max_length=255, blank=True)
    lastname = models.CharField(max_length=255, blank=True)

    uid = models.CharField(max_length=500, primary_key=True, editable=False)

    is_admin = models.BooleanField(default=False)

    role = models.CharField(max_length=1, default='u', choices=ROLES)
    objects = AccountManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']