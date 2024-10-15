from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    email = models.EmailField('email address',unique=True)

    # Especificar related_name personalizado para evitar conflictos
    groups = models.ManyToManyField(Group, through='UserGroup', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, through='UserPermission', related_name='custom_user_permissions')
    
    objects = CustomUserManager()
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name='user'
        verbose_name_plural='users'
        unique_together = ('username', 'email')
        
    def __str__(self, *args, **kwargs):
        return '{}'.format(self.username)
    
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    